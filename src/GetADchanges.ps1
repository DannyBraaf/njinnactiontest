$result = Add-ADPrincipalGroupMembership -Identity $object -MemberOf $group -PassThru
Write-Host "Successfully added '$object' to group '$group'"