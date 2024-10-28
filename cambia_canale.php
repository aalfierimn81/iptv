<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $canale = htmlspecialchars($_REQUEST['canale']);
  if (empty($canale)) {
//    echo "Name is empty";
  } else {
//    echo $canale;
  }

$pid_vlc = exec("pidof vlc");
if ($pid_vlc == "")
{
}
else
{
exec ("kill " . $pid_vlc);
}

sleep (2);
 $comando = "cvlc 'file:///var/www/html/tv/" . $canale ."' --sout '#chromecast' --sout-chromecast-ip=192.168.178.27 --demux-filter=demux_chromecast"; 

//echo ($canale);

//$comando = "cvlc 'file:///var/www/html/tv/channels/1/DasErste.m3u'"; 
//$comando = $comando . " " . "--sout '#chromecast' --sout-chromecast-ip=192.168.178.27 --demux-filter=demux_chromecast";
echo($comando);

pclose(popen($comando, "r"));
}
?>
