#! /usr/local/bin/perl



$body = '<body bgcolor="#007f7f" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">';
$bbstitle ="あやしい＠ぴかちゅ";
$bbsurl = "pikachu.cgi";


$logdir = '../../pikachulog/';



# 時差 サーバの時計がずれてる時や日本時間以外にしたい時に使う
$tim = 0;

$\ = "\n";

	&error(0) if(!opendir(DIR, $logdir));

	@files=readdir(DIR);
	closedir(DIR);

               @files = sort by_number @files;
               $end = @files;
               $end--; 

	print "Content-type: text/html\n\n";
	print "<html><head><title>$bbstitle 過去ログ</title></head>\n";
	print "$body\n";
	print "<center>\n";

	print "<form method=get action=\"$cgiurl\">";
	print "<input type=hidden name=\"action\" value=\"$action\">";
	print "<h2 align=center>$bbstitle過去ログ</h2>";
	print "<table border=1 width=50%>";
	print "<tr><td width=50%>ファイル名</td><td align=right width=20%>サイズ</td><td align=center width=30%>日付</td></tr>";
	foreach (0 .. $end) {
		if (!($files[$_] eq "." or $files[$_] eq "..")) {
			($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks) = stat "$logdir$files[$_]";
			($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime($mtime + 32400 + $tim);
			$mon++;
			$mon = "0$mon" if ($mon < 10);
			if ($mday < 10)  { $mday  = "0$mday";  }
			if ($min < 10)  { $min =  "0$min";  }
			if ($hour < 10) { $hour = "0$hour"; }
			print "<tr><td><a href=\"$logdir$files[$_]\">$files[$_]</a></td>";
			print "<td align=right>$size</td><td align=center>$mon/$mday $hour:$min</td></tr>";
		}
	}
	print "</table>";
	print "<p align=center><a href=\"$bbsurl\">$bbstitle</a></p>";
	print "<h4 align=right>Getdir Ver0.01</h4>";
	print "</body></html>";


sub by_number {
	$a <=> $b;
}


sub error {

	$error = $_[0];
	if    ($error == 0) { $errmsg = '記録ファイルの入出力にエラーが発生しました。'; }
	elsif ($error == 1) { $errmsg = "投稿画面のＵＲＬが<br>$cgiurl<br>" . '以外からの投稿はできません。'; }
	elsif ($error == 2) { $errmsg = "ログファイルがオープンできませんでした。"; }
	elsif ($error == 3) { $errmsg = "投稿間隔が短すぎます。$interval秒お待ちください。"; }

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
	print "<h1>$errmsg</h1>\n";
	print "</body></html>\n";
	exit;
}