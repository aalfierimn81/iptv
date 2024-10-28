<?php
$pid_vlc = exec("pidof vlc");
if ($pid_vlc == "")
{
}
else
{
exec ("kill " . $pid_vlc);
}

sleep (2);
//echo ($canale);

//$comando = "cvlc 'file:///var/www/html/tv/channels/1/DasErste.m3u'"; 
//$comando = $comando . " " . "--sout '#chromecast' --sout-chromecast-ip=192.168.178.27 --demux-filter=demux_chromecast";

?>
