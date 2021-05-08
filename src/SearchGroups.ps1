$parameters = @{}

Write-Host "Searching for AD Groups matching LDAP query: $ldap_query"

$parameters['LDAPFilter'] = $ldap_query 
if ($properties) {
    Write-Host "Selecting properties: $properties"
    $parameters['Properties'] = $properties.Split(",").Trim()
}

$result = Get-ADGroup @parameters
if (-not ($result -is [array])) {
    $result = @($result)
}
Write-Host "Found $($result.Count) matching Group object(s)"
