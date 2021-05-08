import json
import os
import pathlib
import subprocess
import sys


class RunPowershellScript:
    """
    Compiles a Powershell batch script from header, input, actual script and footer
    The actual script is looked up by class name from a ps1 file
    by default stop on script error
    """

    def write_script(self, input=dict(), header="", footer="", end="\r\n"):
        """
        Writes the script content to a file in the current directory
        """
        script_out = ""
        abspath = os.path.abspath(os.path.join("script.ps1"))

        ps1 = os.path.join(
            pathlib.Path(__file__).parent.absolute(), f"{type(self).__name__}.ps1"
        )
        with open(ps1, "r") as script_file:
            script = script_file.read()

        # first normalize line separator, then change if required
        script = script.replace("\r", "")
        script = script.replace("\n", end)

        if header:
            script_out = header

        if input:
            for k, v in input.items():
                if isinstance(v, str):
                    # double quotations to preserve literal value
                    v = v.replace("'", "''")
                    script_out += f"${k} = '{v}'{end}"
                elif isinstance(v, bool):
                    if v:
                        script_out += f"${k} = $TRUE{end}"
                    else:
                        script_out += f"${k} = $FALSE{end}"
                elif isinstance(v, int):
                    script_out += f"${k} = {v}{end}"
                else:
                    script_out += f"${k} = '{v}'{end}"

        script_out += script

        if footer:
            script_out += footer

        with open(abspath, "w") as fp:
            fp.write(script_out)

        return abspath

    def run(self):
        result = None

        script_header = (
            """$ErrorActionPreference = 'Stop'"""
            + "\r\n"
            + """$result = @{}"""
            + "\r\n"
            + """$working_dir = $PWD.Path"""
            + "\r\n"
        )
        script_footer = (
            "\r\n"
            + """$result_json = ConvertTo-Json $result"""
            + "\r\n"            
            + """$result_json | Out-File -FilePath $working_dir\\njinn_result.json -Encoding UTF8 """
        )

        script = self.write_script(
            self.__dict__, header=script_header, footer=script_footer
        )
        # windows needs quotes for path names with spaces
        cmd = f'powershell.exe -NonInteractive -ExecutionPolicy Bypass -File "{script}"'
        sys.stdout.flush()
        proc = subprocess.run(
            cmd,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True,
            encoding="utf_8",
            errors="replace",
        )
        proc.check_returncode()

        try:
            with open("njinn_result.json", encoding="utf-8-sig") as result_file:
                result = json.load(result_file)
        except:
            pass

        return result


class CreateUser(RunPowershellScript):
    def __init__(self):
        self.name = ""
        self.samaccountname = ""
        self.userprincipalname = ""
        self.accountpassword = ""
        self.givenname = ""
        self.surname = ""
        self.displayname = ""
        self.description = ""
        self.path = ""
        self.otherattributes = ""

    def run(self):
        if not self.name and not self.samaccountname and not self.userprincipalname:
            raise Exception(
                "Provide at least a Name, SamAccountName or UPN for the new user."
            )
        if not self.accountpassword:
            raise Exception("Provide a one time password for initial logon.")

        user = super().run()
        result = {"user": user}

        return result


class AddToGroup(RunPowershellScript):
    def __init__(self):
        self.object = ""
        self.group = ""

    def run(self):
        if not self.object:
            raise Exception("Provide an identity of the object to add to group.")
        if not self.group:
            raise Exception("Provide a group to add the object to.")

        object = super().run()
        result = {"object": object}

        return result


class SearchUsers(RunPowershellScript):
    def __init__(self):
        self.ldap_query = ""
        self.properties = ""

    def run(self):
        if not self.ldap_query:
            raise Exception("Provide an LDAP query for the search.")

        users = super().run()
        result = {"users": users}

        return result


class SearchGroups(RunPowershellScript):
    def __init__(self):
        self.ldap_query = ""
        self.properties = ""

    def run(self):
        if not self.ldap_query:
            raise Exception("Provide an LDAP query for the search.")

        groups = super().run()
        result = {"groups": groups}

        return result