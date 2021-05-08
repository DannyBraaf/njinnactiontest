$parameters = @{}

if($name){
    $parameters['Name'] = $name
}
if($samaccountname){
    $parameters['SamAccountName'] = $samaccountname
}
if($userprincipalname){
    $parameters['UserPrincipalName'] = $userprincipalname
}

$parameters['AccountPassword'] = (ConvertTo-SecureString -AsPlainText $accountpassword -Force)

if($path){
    $parameters['Path'] = $path
}
$parameters['GivenName'] = $givenname
$parameters['Surname'] = $surname
$parameters['DisplayName'] = $displayname
$parameters['Description'] = $description
$parameters['ChangePasswordAtLogon'] = $true
$parameters['Enabled'] = $true 

if ($otherattributes) {
    $oa_customobject = ConvertFrom-Json $otherattributes
    $oa_hashtable = @{}
    #The below only processes single level input, as ConvertFrom-Json supports AsHashtable flag only from ps6 onwards
    $oa_customobject.psobject.properties | ForEach-Object { $oa_hashtable[$_.Name] = $_.Value }
    $parameters['OtherAttributes'] = $oa_hashtable
}

$result = New-ADUser @parameters -PassThru
Write-Host "User $result successfully created"
