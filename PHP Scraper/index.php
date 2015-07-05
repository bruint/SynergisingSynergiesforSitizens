<?
// Include OAuth Library
include("src/Google/autoload.php");




/*
This function outputs all features within a Vector set ID. It wil come in the form of JSON.

Simply provide the data link ID
 */
function pullAllFeatures ($id, $nextPageToken) {
	// SET THIS BULLSHIT
	// This is on the Google Dev Console
	// Tom
	$client_email = '327520421254-1gcj9sotk4abkr589115i6am9ss5kjb9@developer.gserviceaccount.com';

	//Harrison
	//$client_email = '483028855196-f0o84fsn40sikn5hs7c0c08tbp7bcciu@developer.gserviceaccount.com';
	// This is downloaded from the Google Dev Console
	//Tom
	$private_key = file_get_contents('SLIP-0bff6b7dca5e.p12');

	//Harrison
	//$private_key = file_get_contents('API Project-3c6837997fd7.p12');
	// STOP SETTING BULLSHIT

	$scopes = array('https://www.googleapis.com/auth/mapsengine.readonly');
	$credentials = new Google_Auth_AssertionCredentials(
	    $client_email,
	    $scopes,
	    $private_key
	);

	$client = new Google_Client();
	$client->setAssertionCredentials($credentials);
	if ($client->getAuth()->isAccessTokenExpired()) {
	  $client->getAuth()->refreshTokenWithAssertion();
	}

	$mapsEngine = new Google_Service_MapsEngine($client);

	if($nextPageToken == "Go"){
		$optParams = array('maxResults' => 1000, 'version' => 'published');
	} else { 
		$optParams = array('maxResults' => 1000, 'version' => 'published', 'pageToken' => $nextPageToken);
	}
	$results = $mapsEngine->tables_features->listTablesFeatures($id, $optParams);

	$nextPageToken = $results->nextPageToken;

	// This needs to be structured properly.
	$returnString = "";
	foreach($results->getFeatures() as $feature) {
		
		$returnString .= json_encode($feature, JSON_PRETTY_PRINT, 512);
		$returnString .= json_encode($feature["modelData"], JSON_PRETTY_PRINT, 512);
	}

	return array($nextPageToken,$returnString);
}

$nextPageToken = "Go";
$runs = 0;
while ($nextPageToken != NULL) {

	$result = pullAllFeatures("09372590152434720789-09942584672885278221", $result[0]);

	file_put_contents("features.json", $result[1], FILE_APPEND);
	
	$runs++;

	if ($runs == 4){
		break;
	}
}


?>