$DCs = Get-ADDomainController -Filter *  -server $server_name

$startDate = (get-date).AddDays(-$days_past)

foreach ($DC in $DCs){
$events = Get-Eventlog -LogName Security -ComputerName $DC.Hostname -after $startDate | Where-Object {$_.eventID -eq 4728 -or $_.eventID -eq 4729}}

 foreach ($e in $events){
    

    if (($e.EventID -eq 4728 )){
        $result["ADchanges"] += "<li>"+$e.TimeGenerated+"--"+$e.ReplacementStrings[6]+ " made changes to '" +$e.ReplacementStrings[2]+ "' and added user '" + $e.ReplacementStrings[0] + "'</li>"
  
    }
 
    if (($e.EventID -eq 4729 )) {    
       $result["ADchanges"] += "<li>"+$e.TimeGenerated+"--"+$e.ReplacementStrings[6]+ " made changes to '" +$e.ReplacementStrings[2]+ "' and removed user '" + $e.ReplacementStrings[0] + "'</li>"
    
    }}    