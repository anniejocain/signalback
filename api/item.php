<?php

class Item extends Controller {

    function recent() {
      $f3=$this->framework;
      $db = $f3->get('DB');
      $db_user = $f3->get('DB_USER');
      $db_password = $f3->get('DB_PASSWORD');
      $db_host = $f3->get('DB_HOST');
      
      $FIELDS     = array('link', 'title', 'description', 'creator');
      $JSON = array();
      
      mysql_connect($db_host, $db_user, $db_password)
      or die ("Could not connect to resource");

      mysql_select_db($db)
      or die ("Could not connect to database");
      
      $query = "SELECT * FROM `roundup` LIMIT 0,5";
      $result = mysql_query($query);
      while ($row = mysql_fetch_array($result))
      {
        $_datas   = array($row[1], $row[2], $row[3], $row[4]);
                  
        $_tmparr  = array_combine($FIELDS, $_datas);
        array_push($JSON, $_tmparr);
      }
      
      
      
      $callback = $_GET['callback'];
      header('Content-type: application/json');
      echo $callback . '(' . json_encode($JSON) . ')';
      
      mysql_close();
    }
    
    function new_item() {
      $f3=$this->framework;
      $link = $_REQUEST['link'];
      $title = $_REQUEST['title'];
      $description = $_REQUEST['description'];
      $creator = $_REQUEST['creator'];
      
      $db = $f3->get('DB');
      $db_user = $f3->get('DB_USER');
      $db_password = $f3->get('DB_PASSWORD');
      $db_host = $f3->get('DB_HOST');
        
      mysql_connect($db_host, $db_user, $db_password)
      or die ("Could not connect to resource");

      mysql_select_db($db)
      or die ("Could not connect to database");   
      
      $query = "INSERT INTO `roundup` (`link`, `description`, `creator`, `title`) VALUES ('$link', '$description', '$creator', '$title')";
      $result = mysql_query($query);

      $this->blog();
      
      mysql_close();
    }
    
    function token() {
      $wp_redirect = $f3->get("WP_REDIRECT");
      $wp_client_secret = $f3->get("WP_CLIENT_SECRET");
      $wp_client_id = $f3->get("WP_CLIENT_ID");
      echo "<p><a href='https://public-api.wordpress.com/oauth2/authorize?client_id=$wp_client_id&redirect_uri=$wp_redirect&response_type=code&blog=http://librarylab.law.harvard.edu/blog/'>authorize</a></p>";
      
      $curl = curl_init( "https://public-api.wordpress.com/oauth2/token" );
      curl_setopt( $curl, CURLOPT_POST, true );
      curl_setopt( $curl, CURLOPT_POSTFIELDS, array(
          'client_id' => $wp_client_id,
          'redirect_uri' => $wp_redirect,
          'client_secret' => $wp_client_secret,
          'code' => $_GET['code'], // The code from the previous request
          'grant_type' => 'authorization_code'
      ) );
      curl_setopt( $curl, CURLOPT_RETURNTRANSFER, 1);
      $auth = curl_exec( $curl );
      $secret = json_decode($auth);
      $access_key = $secret->access_token;
      $blog_id = $secret->blog_id;
      echo "<p>Access key acquired! :: $access_key</p><p>Blog ID is $blog_id</p>";
    }
    
    function blog() {
      $f3=$this->framework;
      $db = $f3->get('DB');
      $db_user = $f3->get('DB_USER');
      $db_password = $f3->get('DB_PASSWORD');
      $db_host = $f3->get('DB_HOST');
      $wp_token = $f3->get("WP_TOKEN");
      $wp_blog = $f3->get("WP_BLOG");
      
      $link_list = '';
      
      mysql_connect($db_host, $db_user, $db_password)
      or die ("Could not connect to resource");

      mysql_select_db($db)
      or die ("Could not connect to database");
      
      $query = "SELECT * FROM `roundup` WHERE `posted` = 0 ORDER BY added DESC";
      $result = mysql_query($query);
      $num_rows = mysql_num_rows($result);
      if($num_rows > 4) {
        while ($row = mysql_fetch_array($result)) {
          $link_list .= '<p><a href="' . $row[1] . '">' . $row[2] . '</a>';
          if(strlen($row[3]) > 0)
            $link_list .= '<br>' . $row[3] . ' - ' . $row[4] . '</p>';
          else  
            $link_list .= '</p>';
        }
        
        $posted_query = "UPDATE `roundup` SET `posted` = '1' WHERE `posted` = 0";
        $posted_result = mysql_query($posted_query);
        $title = "Link roundup " . date("F j, Y"); 
        
        $options  = array (
        'http' => 
        array (
          'ignore_errors' => true,
          'method' => 'POST',
          'header' => 
          array (
            0 => "authorization: Bearer $wp_token",
            1 => 'Content-Type: application/x-www-form-urlencoded',
          ),
          'content' => http_build_query(   
            array (
              'title' => $title,
              'content' => $link_list,
              'categories' => 'roundup',
              'status' => 'draft',
            )
          ),
        ),
      );
       
        $context  = stream_context_create( $options );
        $response = file_get_contents(
          "https://public-api.wordpress.com/rest/v1/sites/$wp_blog/posts/new/",
          false,
          $context
        );
        $json = array();
        $json['response'] = "This one tipped the scales!  Check out a new blog post.";
        header('Content-type: application/json');
        echo json_encode($json);
      }
      else {
        $json = array();
        $json['response'] = "Got it, thanks.";
        header('Content-type: application/json');
        echo json_encode($json);
      }
    }

}
?>
