#! /usr/local/bin/perl



$body = '<body bgcolor="#007f7f" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">';
$bbstitle ="���₵�����҂�����";
$bbsurl = "pikachu.cgi";


$logdir = '../../pikachulog/';



# ���� �T�[�o�̎��v������Ă鎞����{���ԈȊO�ɂ��������Ɏg��
$tim = 0;

$\ = "\n";

	&error(0) if(!opendir(DIR, $logdir));

	@files=readdir(DIR);
	closedir(DIR);

               @files = sort by_number @files;
               $end = @files;
               $end--; 

	print "Content-type: text/html\n\n";
	print "<html><head><title>$bbstitle �ߋ����O</title></head>\n";
	print "$body\n";
	print "<center>\n";

	print "<form method=get action=\"$cgiurl\">";
	print "<input type=hidden name=\"action\" value=\"$action\">";
	print "<h2 align=center>$bbstitle�ߋ����O</h2>";
	print "<table border=1 width=50%>";
	print "<tr><td width=50%>�t�@�C����</td><td align=right width=20%>�T�C�Y</td><td align=center width=30%>���t</td></tr>";
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
	if    ($error == 0) { $errmsg = '�L�^�t�@�C���̓��o�͂ɃG���[���������܂����B'; }
	elsif ($error == 1) { $errmsg = "���e��ʂ̂t�q�k��<br>$cgiurl<br>" . '�ȊO����̓��e�͂ł��܂���B'; }
	elsif ($error == 2) { $errmsg = "���O�t�@�C�����I�[�v���ł��܂���ł����B"; }
	elsif ($error == 3) { $errmsg = "���e�Ԋu���Z�����܂��B$interval�b���҂����������B"; }

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
	print "<h1>$errmsg</h1>\n";
	print "</body></html>\n";
	exit;
}