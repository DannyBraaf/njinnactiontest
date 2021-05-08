$parameters = @{}

Write-Host "Searching for AD Users matching LDAP query: $ldap_query"

$parameters['LDAPFilter'] = $ldap_query 
if ($properties) {
    Write-Host "Selecting properties: $properties"
    $parameters['Properties'] = $properties.Split(",").Trim()
}

$result = Get-ADUser @parameters
if (-not ($result -is [array])) {
    $result = @($result)
}
Write-Host "Found $($result.Count) matching User object(s)"
