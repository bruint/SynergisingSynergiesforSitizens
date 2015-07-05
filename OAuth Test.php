<?php
require_once 'google-api-php-client/src/Google/autoload.php';

/**
 * A rough implementation of paging through the GME API to retrieve
 * multiple resultsets.
 *
 * Params:
 * Google_OAuth2 $oauthClient - An OAuth2 Client object.
 * string $url - The complete URL to call include query string params.
 * array $query_params - An array of query string params (name => value) to pass.
 * string $merge_on - Identifies the element in the response that
 *    contains the features or assets list. Typically 'features'.
 */
function gme_paging(Google_Auth_OAuth2 $oauthClient, $url, $query_params = array(), $merge_on) {
    $merged_responses = array();
    do {
        if(isset($responseObj->nextPageToken)) {
            $params["pageToken"] = $responseObj->nextPageToken;
        }
        $start = microtime(true);
        $curl_test = curl_wrapper($oauthClient, $url, $query_params);
        var_dump($curl_test);
        $responseObj = json_decode(curl_wrapper($oauthClient, $url, $query_params));
        $secs_taken = microtime(true) - $start;
        // Google imposes a max queries per second per project of 1 on most queries
        // /table/features queries are allowed higher limits as per https://developers.google.com/maps-engine/new
        // @TODO Make it smart enough to sniff for 'allowed_queries_per_second' in /tables/features responses and adapt.
        if($secs_taken < 1) {
          usleep(1000000 - ($secs_taken * 1000000));
        }
        $merged_responses = array_merge($merged_responses, $responseObj->{$merge_on});
    } while(isset($responseObj->nextPageToken));
    return $merged_responses;
}

/**
 * A generic wrapper for cURL that abstracts away common requirements
 * and issues around using the GME API.
 *
 * Params:
 * Google_OAuth2 $oauthClient - An OAuth2 Client object.
 * string $url - The complete URL to call include query string params.
 * array $options - An additional cURL options to pass through.
 *
 * Notably:
 * - Content-type: application/json for POST requests
 * - Catching rate limit exceeded errors
 */
function curl_wrapper(Google_Auth_OAuth2 $oauthClient, $url, $options = array()) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt_array($ch, $options);
    $headers = array(
        'Authorization: Bearer ' . $oauthClient->getAccessToken()
    );
    // Google accepts POST data as JSON only - no form-encoded input
    if(isset($options[CURLOPT_POST]) && $options[CURLOPT_POST] == true) {
        $headers[] = "Content-Type: application/json";
    }
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    $response = json_decode(curl_exec($ch));
    if(!in_array(curl_getinfo($ch, CURLINFO_HTTP_CODE), array(200, 204))) {
        // You'll want to handle errors...
    }
    if(isset($response->error) && $response->error->errors[0]->reason === "rateLimitExceeded") {
        // If you've can have multiple simultaneous clients you'll probably want to catch
        // and handle rate limit errors. So sleep for an arbitrary period...
        usleep(1000000);
        // ...and try again
    }
    curl_close($ch);
    return $response;
}

// Your Google Developer project details from https://cloud.google.com/console
const SERVICE_APP_NAME = 'api-project-483028855196';
const SERVICE_CLIENT_ID = '483028855196-f0o84fsn40sikn5hs7c0c08tbp7bcciu.apps.googleusercontent.com';
const SERVICE_ACCOUNT_EMAIL = '483028855196-f0o84fsn40sikn5hs7c0c08tbp7bcciu@developer.gserviceaccount.com';
const KEY_FILE = '5bae0f85ba4b.p12';
const SCOPE = 'https://www.googleapis.com/auth/mapsengine.readonly'; // sans .readonly for write operations
/**
 * A simplified version of Google's OAuth for PHP Web Server flow.
 * https://developers.google.com/maps-engine/documentation/oauth/webserver
 *
 * Implements:
 * - Retrieval of access tokens
 * - Refresh of an existing access token
 * - Storage of access tokens in sessions
 *
 * Requirements:
 *   - Google APIs Client Libraries: https://developers.google.com/discovery/libraries
 */
$client = new Google_Client();
$oauthClient = new Google_Auth_OAuth2($client);
$client->setApplicationName(SERVICE_APP_NAME);
$client->setClientId(SERVICE_CLIENT_ID);
$token_name = "oauth_client_" . $client_id . "_token";
$token = (array)json_decode($_SESSION[$token_name]);
if(isset($token["access_token"]) && time() <= ($token["created"] + $token["expires_in"])) {
	$oauthClient->setAccessToken($_SESSION[$token_name]);
} else {
	$oauthClient->refreshTokenWithAssertion(new Google_Auth_AssertionCredentials(
	  SERVICE_ACCOUNT_EMAIL,
	  array(SCOPE),
	  file_get_contents(KEY_FILE)
	));
	$_SESSION[$token_name] = $oauthClient->getAccessToken();
}
if($oauthClient->getAccessToken()) {
	// All good, we've got a valid access token!
    echo 'All good, let\'s go!';
   
    // Set up some variables
    $asset_id = '09372590152434720789-16691395374091854705';
    $token = $oauthClient->getAccessToken();
    print $token;
    $url = 'https://www.googleapis.com/mapsengine/v1/tables/'.$asset_id.'/features?version=published&key='.$token;
    print $url;
    $merge_on = 'features';
    
    // Call a request
    gme_paging($oauthClient, $url, array(), $merge_on);
} else {
	// Uh oh :(
}
?>