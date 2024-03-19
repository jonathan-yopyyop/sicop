from ldap3 import Server, Connection, ALL, SUBTREE
from sicop.maloka_da.models import (
    ActiveDirectoryCredential,
    OrganizationalUnit,
    ActiveDirectoryUser,
)
import os


class ActiveDirectoryUtil:
    __credential = None
    __domain = None
    __domain_extension = None
    __username = None
    __password = None
    __connection = None
    __server = None
    __connection = None

    def __init__(self):
        if ActiveDirectoryCredential.objects.count() > 0:
            self.__credential = ActiveDirectoryCredential.objects.first()
            self.__domain = self.__credential.domain
            self.__domain_extension = self.__credential.domain_extension
            self.__username = self.__credential.username
            self.__password = self.__credential.password
            # self.__server = Server(
            #     f"ldap://{self.__domain}.{self.__domain_extension}",
            #     get_info=ALL,
            # )
            self.__server = Server(
                f"ldap://10.0.1.5",
                get_info=ALL,
            )

    def get_credential(self):
        return self.__credential

    def get_domian(self):
        return self.__domain

    def get_domain_extension(self):
        return self.__domain_extension

    def open_connection(self):
        if ActiveDirectoryCredential.objects.count() > 0:

            self.__connection = Connection(
                self.__server,
                user=self.__username,
                password=self.__password,
                auto_bind=True,
            )
        else:
            self.__connection = None

    def close_connection(self):
        self.__connection.unbind()

    def get_ldap_ous(self):
        self.open_connection()
        if self.__connection is not None:
            try:
                self.__connection.search(
                    search_base=f"dc={self.__domain},dc={self.__domain_extension}",
                    search_filter="(objectClass=organizationalUnit)",
                    search_scope="SUBTREE",
                    attributes=["ou"],
                )
                data_to_store = []
                for entry in self.__connection.entries:
                    splited_entries = entry.entry_dn.split(",")
                    dictionary = {}
                    for splited_enty in splited_entries:
                        key_value = splited_enty.split("=")
                        if key_value[0] == "OU":
                            dictionary[key_value[0]] = key_value[1]
                            if (
                                OrganizationalUnit.objects.filter(
                                    OU=key_value[1],
                                    credential=self.__credential,
                                ).count()
                                == 0
                            ):
                                OrganizationalUnit.objects.create(
                                    credential=self.__credential,
                                    OU=key_value[1],
                                )
                                print(f"OU {key_value[1]} created")
                            else:
                                print(f"OU {key_value[1]} already exists")
                    data_to_store.append(dictionary)
                return data_to_store
            except Exception as e:
                print(e)
                return []
            finally:
                self.close_connection()
        else:
            return []

    def get_ldap_users(self):
        self.open_connection()
        if self.__connection is not None:
            try:
                organizational_units = OrganizationalUnit.objects.filter(
                    credential=self.__credential,
                )
                for organizational_unit in organizational_units:
                    ou = organizational_unit.OU

                    print("------------------------", f"OU: {ou}", "------------------------", sep="\n")
                    try:
                        self.__connection.search(
                            search_base=f"ou={ou},dc={self.__domain},dc={self.__domain_extension}",
                            search_filter="(objectClass=user)",
                            search_scope="SUBTREE",
                            attributes=["sAMAccountName"],
                        )
                        data_to_store = []
                        for entry in self.__connection.entries:
                            dn = entry.entry_dn
                            dn_splited = dn.split(",")
                            name = ""
                            user = ""
                            dictionary = {}
                            for dn_splited_item in dn_splited:
                                key_value = dn_splited_item.split("=")
                                if key_value[0] == "CN":
                                    name = key_value[1]
                                    dictionary["name"] = name
                                if key_value[0] == "OU":
                                    dictionary["organizational_unit"] = organizational_unit

                            if "sAMAccountName" in entry:
                                user = entry["sAMAccountName"]
                            dictionary["user"] = user
                            print("\t", "+++++++++++++++++++++++++++++++++++++++++++++")
                            print("\t", dictionary)
                            print("\t", "+++++++++++++++++++++++++++++++++++++++++++++")
                            data_to_store.append(dictionary)

                        for user in data_to_store:
                            organizational_unit_object = OrganizationalUnit.objects.filter(
                                OU=ou,
                                credential=self.__credential,
                            ).first()
                            if (
                                ActiveDirectoryUser.objects.filter(
                                    user=user["user"],
                                    organizational_unit=organizational_unit_object,
                                ).count()
                                == 0
                            ):
                                ActiveDirectoryUser.objects.create(
                                    organizational_unit=organizational_unit_object,
                                    name=user["name"],
                                    user=user["user"],
                                )
                                print(f"User {user['user']} created")
                            else:
                                print(f"User {user['user']} already exists")

                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)

            finally:
                self.close_connection()

    def validate_credentials(self, user, password):
        try:
            server = Server(
                f"ldap://{self.__domain}.{self.__domain_extension}",
                get_info=ALL,
            )
            print(f"ldap://{self.__domain}.{self.__domain_extension}")
            connection = Connection(
                server,
                user=user,
                password=password,
                auto_bind=True,
            )
            connection.unbind()
            return True
        except Exception as e:
            print(e)
            return False
