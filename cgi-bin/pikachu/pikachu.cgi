#! /usr/bin/perl
#↑はサーバによって違うので適宜変更の事

# SunechamaBBS Ver2.20 ぴかちゅ仕様＋ShibaCounter+1.943

# 開発環境
# AN HTTP Server 1.21c + Perl for Win32 Ver5.00307 + Cygwin Perl Ver5.00562 + Netscape Navigator 4.08(動作確認に使用)



#デフォルトの設定で使う場合(shinさんのツリー表をパクりました。shinさんごめん)
#	|--------- [cgi-bin]（755）
#			|
#			|-- countlog.txt (666)（カウンタのログファイル。デフォルトの設定では必要無い）
#			|-- getdir.cgi (755)（ディレクトリリスト表示スクリプト。ディレクトリリストが表示出来ないサーバ(Virtualave等)用）
#			|-- jcode.pl (755)（日本語コード変換ライブラリ）
#			|-- pikachu.cgi (755)（このスクリプト）
#			|-- pikachu.log (666)（記録ファイル）
#			|-- time.txt (666)（投稿時間記録ファイル。連続投稿を防止するのに使用）
#			|
#			|--[count](777)
#			|    |
#			|    |--count?.txt(666)（アクセスカウンタファイル。 count0～$countlevel-1.txtを置く。）
#			|    |--day.txt(666)（一日のアクセス数とOSやブラウザ別のカウンタファイル。ロック処理やミラーリングは一切してないので壊れやすい）
#			|
#			|--[log](755)ログファイル保存ディレクトリ
#			     |
#			     |--年月.html(666)もしくは年月日.html(666)(過去ログファイル)
#			     |			たとえば1999年12月なら、年=1999 月=12、つまり199912.htmlを置く。
#			     |			空ファイルでいい。
#			     |			logディレクトリのパーミッションが7x7だとファイルを置かなくても自動的に作成するみたい。






$title = 'あやしい＠ぴかちゅ';

# body部
$bgc    = '004040';
$textc  = 'ffffff';
$linkc  = 'eeffee';
$vlinkc = 'dddddd';
$alinkc = 'ff0000';

# 表示件数
$def = 30;

# 最大保存件数
$max = 300;

$fontsize = 2;

# 時差 gmtime関数から日本時間を得ているので、投稿時間を日本時間以外にしたい時と
# サーバの内蔵時計がずれてる時以外は0でいい。
$tim = 0;

#最大行数
$maxrow = 7;

# -------------------------------------------- カウンタ --------------------------------------------
# カウンタの強度
$countlevel = 2;
$countfile = './count/count';
$countfiledat = '.txt';
$countdate = '99/04/20';

$daycount = './count/day.txt';



# このスクリプト 単に $cgiurl = 'pikachu.cgi'; でもいいが、フルパスを入れたほうがいいかも
$cgiurl = 'pikachu.cgi';

#サポート掲示板のURL　無い場合は空欄（ $supporturl = ''; ）にする。
$supporturl = 'http://8616.teacup.com/gmama/bbs';


# 管理人のメールアドレス　無い場合は空欄（ $mailadd = ''; ）にする。
$mailadd = 'webmaster@nelii.ducub.com';

# ------------------------------------ ディレクトリ・ファイル名 ------------------------------------
# 日本語コード変換ライブラリjocde.plのパス
# 一段上のディレクトリに置く場合は require '../jcode.pl'; にする
require '../jcodeLE.pl';

# 内容が書き込まれる記録ファイルのパスを設定
$file = './pikachu.log';

# 別途とるログの保存先ディレクトリ・ファイル名先頭文字・拡張子の指定
$logdir ='../../pikachulog/';
$logfile = ''; # $logfile = 'pikachu' 
$logfiledat = '.html';

#最近の過去ログの場所
#getdir.cgiを使わない場合は $logpath = $logdir; にする
$logpath = './getdir.cgi';



#ログファイルの罫線
# $border = "--------------------------------------------------------------------------------\n";
$border = '<hr>';


# 投稿時間記録ファイルのパス
$timefile = './time.txt';
# 連続投稿制限時間（秒）
# 必要無い時は0にする
$interval = 60;


# 入力形式の設定
$method = 'post';

$action = 'thunder';

# 時刻処理
($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = gmtime(time+32400+$tim);
$month++;

$youbi = ('Sun','Mon','Tues','Wed','Thursday','Friday','Saturday') [$wday];
$month = "0$month" if ($month < 10);
$mday = "0$mday" if ($mday < 10);
$hour = "0$hour" if ($hour < 10);
$min = "0$min" if ($min < 10);
$sec = "0$sec" if ($sec < 10);

$year += 1900;

# 時刻フォーマット
$date = "$year/$month/$mday ($youbi) at $hour:$min:$sec";

# ログファイル名取得
# 書き込みが多いときは $filedate = "$logdir$logfile$year$month$mday$logfiledat"; にする
$filedate = "$logdir$logfile$year$month$logfiledat";

if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

@argv = split(/&/,$buffer);
foreach (@argv) {
	($name, $value) = split(/=/);

	$value =~ tr/+/ /;

	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ s/\t/        /g;

	&jcode'convert(*value,'sjis');
	$value =~ s/\n//g;
	

	$MSG{$name} = $value;
}



$def = $MSG{'def'} if ($MSG{'def'} ne '');
$defnext = $def;
#if ($defnext > $defmax) {$defnext = $defmax;}

$bgc = $MSG{'bgcolor'} if ($MSG{'bgcolor'} ne '');
$textc = $MSG{'textcolor'} if ($MSG{'textcolor'} ne '');
$bgc = $MSG{'bgcolor'} if ($MSG{'bgcolor'} ne '');
$fontsize = $MSG{'fontsize'} if ($MSG{'fontsize'} ne '');
$fontsize = 2 if ($fontsize > 7 || $fontsize < 1);

$body  = "<body bgcolor=\"#$bgc\" text=\"#$textc\" link=\"#$linkc\" vlink=\"#$vlinkc\" alink=\"#$alinkc\">";

&confirm if ( ($MSG{'confirm'} ne '') && ($MSG{'value'} ne ""));
if (($MSG{'action'} eq "$action") && ($MSG{'value'} ne ""))  { &regist; }
&html;

sub html {

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";


#	バナ―はここかprint "</body></html>\n";の一行上に書く

#	print "<!--#echo banner=\"\"-->";

	print "<hr>\n";

	print "<font size=+1><b>$title</b></font>\n";
	print "<font size=-1><b><a href=\"mailto:$mailadd\">Contact</a> " if ($mailadd ne '');
	print "<a href=\"$supporturl\">Support Bulletin Board</a>" if ($supporturl ne '');

	print "</b></font>\n";
	&printform;
	if ( $countlevel > 0 ){
		print "From $countdate ";
		&counter;
	}
	print "<hr>\n";
	print '<table border="0" cellpadding="1" cellspacing="0" width="99%"><tr bgcolor="#004040"><td>';
	print "\n<a href=\"http://meiso.s147.xrea.com/p/pbbs.cgi\">Pikachu@Meiso</a>｜\n";
	print "<a href=\"http://www.org1.com/~osamu/pbbs.cgi\">Pikachu@Meiso\<font size=-1><sup>TM</sup></font></a><p>\n";
	print "<font color=white>The recent logs are </font><a href=\"./$logpath\">here</a></td></tr></table>\n";



	if (!open(DB,"$file")) { &error(0); }
	@lines = <DB>;
	close(DB);
	print "<font size=$fontsize><pre>\n";

	if ($MSG{'page'} eq '') { $page = 0; } else { $page = $MSG{'page'}; }
	$linecount = @lines;
	$linecount--;
	$p_end = $page + $def - 1;
	$p_end = $linecount if ($p_end > $linecount);
	foreach ($page .. $p_end) {

		($date,$m1,$m2,$m3,$m4,$m5,$m6,$m7, $random) = split(/\t/,$lines[$_]);

		print "<hr>Posted：$date\n";

		&getpika;
		print @pikachiu;
		splice( @pikachiu, 0);

	}

	$p_next = $p_end + 1;
	$s = $page + 1;
	$e = $p_end + 1;
	$linecount++;
	if ($end < 0) { print"<hr>No post available"; }
	else { print "<hr>New Arrivals $s-$e (Number of records $linecount Maximum number of records $max）</pre><p>\n"; }
	if ($p_end ne ($linecount - 1)) {
		print "<form method=$method action=\"$cgiurl\">\n";
		print "<input type=hidden name=\"page\" value=\"$p_next\">\n";
		print "<input type=hidden name=\"def\" value=\"$def\">\n";
		print "<input type=hidden name=\"bgcolor\" value=\"$bgc\">\n";
		print "<input type=hidden name=\"textcolor\" value=\"$textc\">\n";
		print "<input type=hidden name=\"fontsize\" value=\"$fontsize\">\n";
		print "<input type=submit value=\"Next\"></form>\n";
	}
	print "<h4 align=right><a href=\"http://www.oocities.com/Tokyo/Dojo/5886/cgi/index.html\">SunechamaBBS</a> Ver2.30 Pikachu Spec＋ShibaCounter+1.943</h4>\n";
	print "</body></html>\n";
	exit;
}

sub confirm {
	@msgs = split(/\r/,$MSG{'value'});

	foreach (0 .. $maxrow - 1) {
		$msgs[$_] =~ s/\s/ /g;
		$len = length($msgs[$_]);
		$msgs[$_] = substr( "$msgs[$_]                        ", 0, 24);
		$msgs[$_] =~ s/&/&amp\;/g;
		$msgs[$_] =~ s/</&lt\;/g;

	}
	print "Content-type: text/html\n\n";
	print "<html><head><title>Table Confirmation</title></head>\n";
	print "$body\n";
	print "<pre>";
	print "Sentences typed by Anta\n";
	print "----------------------------------------\n";
	print $MSG{'value'};
	print "\n----------------------------------------\n";
	print "\n\n<pre>Actual table text\n";
	print " ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n";
	print "｜ $msgs[0] ｜\n";
	print "｜ $msgs[1] ｜\n";
	print "｜ $msgs[2] ｜\n";
	print "｜ $msgs[3] ｜\n";
	print "｜ $msgs[4] ｜\n";
	print "｜ $msgs[5] ｜\n";
	print "｜ $msgs[6] ｜\n";
	print " ＼＿＿＿＿＿＿＿＿＿＿＿＿／</pre>\n";
	print "<form method=$method action=\"$cgiurl\">\n";
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "<textarea name=\"value\" rows=7 cols=24>$MSG{'value'}</textarea><br>\n";
	print "<input type=hidden name=face value=$MSG{'face'}>";
	print "Total\n";
	print "<input type=text name=\"def\" size=3 value=\"$def\" maxlength=3>\n";
	print "BG Color\n";
	print "<input type=text name=\"bgcolor\" size=6 value=\"$bgc\">\n";
	print "Textカラー\n";
	print "<input type=text name=\"textcolor\" size=6 value=\"$textc\">\n";
	print "font size\n";
	print "<input type=text name=\"fontsize\" size=2 value=\"$fontsize\" maxlength=1><br>\n";
	print "<input type=submit value=\"Submit\"><input type=reset value=\"Reset\"><p>\n";

	print "</form></body></html>\n";
	exit;
}

sub printform {
	print "<form method=$method action=\"$cgiurl\">\n";
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "<table><tr><td>\n";
	print "<textarea name=\"value\" rows=7 cols=24></textarea></td>\n";
	print "<td valign=bottom><pre>\n";
	print " 　　 /|　 /|\n";
	print "　　 / |　/ |\n";
	print "　　/　⌒　　\n";
	print "＞ /●_　●　\n";
	print "　(〇 ～　〇 </pre></td>";
	print "<td valign=bottom><pre>　　　　 　　　∨\n";
	print "　　　▲　　　　　▲\n";
	print "　　　＼＼＿＿＿／／\n";
	print "　／＼ /　　　　 ＼ \n";
	print "　＼　｜　●　．●｜\n";
	print "　　＼｜○　　～　○\n";
	print "　　／▼∋　　　　∋\n";
	print "　　＼▼　　　　　｜\n";
	print "　　　｜＿〇＿＿＿〇\n";
	print "</pre></td>\n";
	print "<td valign=bottom><pre>";
	print "　▼＼＿＿_／▼　＿＿\n";
	print "　 ＼　　　 ／ ／　／\n";
	print "＞  /●｡ ● ＼ ＼　＼\n";
	print "　（） ～　○ ＼/　／\n";
	print "</pre></td></tr>\n";
	print "<tr><td><input type=checkbox name=confirm value=checked checked>Table Confirmation</td>\n";
	print "<td align=center><input type=radio name=face value=0 checked></td>\n";
	print "<td align=center><input type=radio name=face value=200></td>\n";
	print "<td align=center><input type=radio name=face value=201></td>\n";
	print "</tr></table>\n";
	print "The maximum length is 24 single-byte characters (12 double-byte characters) x 7 lines. Any more than that will be truncated.<p>\n";
	print "Total\n";
	print "<input type=text name=\"def\" size=3 value=\"$def\" maxlength=3>\n";
	print "BGカラー\n";
	print "<input type=text name=\"bgcolor\" size=6 value=\"$bgc\">\n";
	print "Textカラー\n";
	print "<input type=text name=\"textcolor\" size=6 value=\"$textc\">\n";
	print "font size\n";
	print "<input type=text name=\"fontsize\" size=2 value=\"$fontsize\" maxlength=1>\n";
	print "<a href=\"$cgiurl?bgcolor=$bgc\&textcolor=$textc\&def=$def\&fontsize=$fontsize\">Bookmark</a><br>\n";
	print "If the fixed-pitch font is set correctly, but it is misaligned, try changing the <b>font size</b> above.<p>\n";
	print "<input type=submit value=\"Post\Reload\"><input type=reset value=\"Reset\"><p>\n";
	print "</form>\n";

}


sub normal {

	if ($random == 0 ) { $eye = "●_　●"; }
	else { $eye = "☆_　★ ﾋﾟｶｯ"; }

	push( @pikachiu, "\n"
			," ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
			,"｜ $m1 ｜\n"
			,"｜ $m2 ｜\n"
			,"｜ $m3 ｜\n"
			,"｜ $m4 ｜　　 /|　 /|\n"
			,"｜ $m5 ｜ 　 / |　/ |\n"
			,"｜ $m6 ｜　 /　⌒　　\n"
			,"｜ $m7  ＞ /$eye \n"
			," ＼＿＿＿＿＿＿＿＿＿＿＿＿／　(〇 ～　〇\n"
	)
}

sub normal2 {


	push( @pikachiu, "\n"

			," ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
			,"｜ $m1 ｜\n"
			,"｜ $m2 ｜\n"
			,"｜ $m3 ｜\n"
			,"｜ $m4 ｜\n"
			,"｜ $m5 ｜\n"
			,"｜ $m6 ｜\n"
			,"｜ $m7 ｜\n"
			," ＼＿＿＿＿＿＿　＿＿＿＿＿／\n"
			,"　　　　 　　　∨\n"
			,"　　　▲　　　　　▲\n"
			,"　　　＼＼＿＿＿／／\n"
			,"　／＼ /　　　　 ＼\n"
			,"　＼　｜　●　．●｜\n"
			,"　　＼｜○　　～　○\n"
			,"　　／▼∋　　　　∋\n"
			,"　　＼▼　　　　　｜\n"
			,"　　　｜＿〇＿＿＿〇\n"
	)
}



sub normal3 {


	push( @pikachiu, "\n"

		," ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"｜ $m1 ｜\n"
		,"｜ $m2 ｜\n"
		,"｜ $m3 ｜\n"
		,"｜ $m4 ｜\n"
		,"｜ $m5 ｜▼＼＿＿_／▼　＿＿\n"
		,"｜ $m6 ｜ ＼　　　 ／ ／　／\n"
		,"｜ $m7  ＞ /●｡ ● ＼ ＼　＼\n"
		," ＼＿＿＿＿＿＿＿＿＿＿＿＿／ （） ～　○ ＼/　／\n"
	)
}


sub pika001 {
push( @pikachiu, "\n"
		," ／￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"｜$m1｜\n"
		,"｜$m2｜\n"
		,"｜$m3｜\n"
		,"｜$m4 ＞ ＞◎\n"
		,"｜$m5｜　（　ヽ\n"
		,"｜$m6｜　　＼&lt;&lt;）\n"
		,"｜$m7｜　　　｜　＼\n"
		," ＼＿＿＿＿＿＿＿＿＿＿＿／ 　　　∧\n"
)
}

sub pika002 {

push( @pikachiu, "┏━━━┓┏━━━┓┏━━━┓┏━━━┓┏━━━┓┏━━━┓┏━━━┓\n"
		,"┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃\n"
		,"┗━━━┛┗━━━┛┗━━━┛┗━━━┛┗━━━┛┗━━━┛┗━━━┛\n"
		,"┏━━━┓　　 ／￣￣￣￣￣￣￣￣￣￣￣￣＼　　　　　　　　 ┏━━━┓\n"
		,"┃ＩＣＱ┃　　｜ $m1 ｜　　　　　　　　┃ＩＣＱ┃\n"
		,"┗━━━┛　　｜ $m2 ｜　　　　　　　　┗━━━┛\n"
		,"┏━━━┓　　｜ $m3 ｜　　　　　　　　┏━━━┓\n"
		,"┃ＩＣＱ┃　　｜ $m4 ｜　　 /|　 /|　　┃ＩＣＱ┃\n"
		,"┗━━━┛　　｜ $m5 ｜ 　 / |　/ |　　┗━━━┛\n"
		,"┏━━━┓　　｜ $m6 ｜　 /　⌒　　　　┏━━━┓\n"
		,"┃ＩＣＱ┃　　｜ $m7　＞ /＞ 　＜；　　┃ＩＣＱ┃\n"
		,"┗━━━┛　　 ＼＿＿＿＿＿＿＿＿＿＿＿＿／　(〇 Д　〇　　 ┗━━━┛\n"
		,"┏━━━┓┏━━━┓┏━━━┓┏━━━┓┏━━━┓┏━━━┓┏━━━┓\n"
		,"┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃┃ＩＣＱ┃\n"
		,"┗━━━┛┗━━━┛┗━━━┛┗━━━┛┗━━━┛┗━━━┛┗━━━┛\n"
)
}

sub pika003 {

push( @pikachiu, "\n"
		,"　　　　　　　　 ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"　　　　　　　　｜ $m1 ｜\n"
		,"　　　　　　　　｜ $m2 ｜\n"
		,"　　　　　　　　｜ $m3 ｜\n"
		,"　　　　　　　　｜ $m4 ｜\n"
		,"　　　　　　　　｜ $m5 ｜\n"
		,"　　　　 ∧ ∧　｜ $m6 ｜\n"
		,"～′￣￣(´ー`)＜  $m7 ｜\n"
		,"  UU￣￣ U  U　　＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
)
}

sub pika004 {

push( @pikachiu, " 　＿＿＿＿＿＿＿＿＿＿＿＿\n"
		," ／　　　　　　　　　　　　＼\n"
		,"｜ $m1 ｜\n"
		,"｜ $m2 ｜\n"
		,"｜ $m3 ｜\n"
		,"｜ $m4 ｜\n"
		,"｜ $m5 ｜\n"
		,"｜ $m6 ｜\n"
		,"｜ $m7 ｜\n"
		," ＼＿＿＿＿　＿＿＿＿＿＿＿／\n"
		,"　　　　　 ∨\n"
		,"　～ ヽ(´Д`)ノ く Good night~!\n"
		,"　～ 　（　　）　～\n"
		,"　～ 　ノ ωヽ　 ～\n"
)
}

sub pika005 {

push( @pikachiu, " 　＿＿＿＿＿＿＿＿＿＿＿＿\n"
		," ／　　　　　　　　　　　　＼\n"
		,"｜ $m1 ｜\n"
		,"｜ $m2 ｜\n"
		,"｜ $m3 ｜　　 ▲\n"
		,"｜ $m4 ｜　／＜＞＼\n"
		,"｜ $m5 ｜　∈◎◎∋\n"
		,"｜ $m6  ＞　∥Θ∥\n"
		,"｜ $m7 ｜　　＼∴＼\n"
		," ＼＿＿＿＿＿＿＿＿＿＿＿＿／　　　 ＼∴＼\n"
)
}

sub pika006 {
push( @pikachiu, "　　　　　　　　　　　　　　　　　　　｜｜｜｜｜\n"
		," 　＿＿＿＿＿＿＿＿＿＿＿＿　　　　 ／￣￣￣￣￣＼\n"
		," ／　　　　　　　　　　　　＼　　 ／　　　　　　　＼\n"
		,"｜ $m1 ｜　 │　／　　　　＼　│\n"
		,"｜ $m2 ｜ ／│　　━　　━　　│＼\n"
		,"｜ $m3 ｜│ │　　　││　　　│ │\n"
		,"｜ $m4 ｜ ＼│　　　││　　　│／\n"
		,"｜ $m5 ｜　 │　　（　　）　　│\n"
		,"｜ $m6 ｜　 │　　 ＿＿＿ 　　│\n"
		,"｜ $m7  ＞　│　　 ＼＿／　　 │\n"
		," ＼＿＿＿＿＿＿＿＿＿＿＿＿／ 　ノ＼　　　　　　　／ヽ\n"
		,"　 　　　　　　　　　　　　　　　 ノ＼＿＿＿＿＿／ヽ\n"
)
}

sub pika007 {


push( @pikachiu, "\n"
		," ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"｜ $m1 ｜\n"
		,"｜ $m2 ｜\n"
		,"｜ $m3 ｜\n"
		,"｜ $m4 ｜\n"
		,"｜ $m5 ｜\n"
		,"｜ $m6 ｜\n"
		,"｜ $m7 ｜\n"
		," ＼＿＿＿＿＿＿　＿＿＿＿＿／\n"
		," 　　　　　　　∨\n"
		,"　　　 ／￣＼＿＿＿／￣＼\n"
		,"　　 ／ ／＼　〈〉　／＼ ＼\n"
		,"　　｜／ 　｜●　●｜　 ＼｜\n"
		,"　　｜ＷＷ≪≡ ∀ ≡≫ＷＷ｜\n"
		,"　　｜ ／ （￣￣￣￣） ＼ ｜\n"
		,"　　 Ｗ　 ／||ＷＷ||＼　 Ｗ\n"
		,"　　　　 ｜ Ш　　Ш ｜\n"
		,"　 ／￣￣￣　　∧　　￣￣￣＼\n"
		," 　￣￣￣￣￣￣　￣￣￣￣￣￣\n"
)
}

sub pika008 {

push( @pikachiu, "　　　　　　　　 ▲　　　　　　　▲\n"
		,"　　　　　　　／＜＞＼　 ▲ 　／＜＞＼\n"
		,"　　　　　　　∈◎◎∋／＜＞＼∈◎◎∋\n"
		,"　　　　　　 ▲∥Θ∥ ∈◎◎∋ ∥Θ∥▲\n"
		,"　　　　　／＜＞＼　 ▲∥Θ∥▲ 　／＜＞＼\n"
		,"　　　　　∈◎◎∋／＜＞＼／＜＞＼∈◎◎∋\n"
		,"　　　　 ▲∥Θ∥ ∈◎◎∋∈◎◎∋ ∥Θ∥▲\n"
		,"　　　／＜＞＼ 　▲∥Θ∥　∥Θ∥▲　 ／＜＞＼\n"
		,"　　　∈◎◎∋／＜＞＼　 ▲ 　／＜＞＼∈◎◎∋\n"
		,"　　　 ∥Θ∥ ∈◎◎∋／＜＞＼∈◎◎∋ ∥Θ∥\n"
		,"　　　　＼∴＼ ∥Θ∥ ∈◎◎∋ ∥Θ∥ ／∴／\n"
		,"　 ▲　　 ＼∴＼＼∴＼ ∥Θ∥ ／∴／／∴／ 　　▲\n"
		,"／＜＞＼　　＼∴＼＼∴￣《》￣∴／／∴／　　／＜＞＼\n"
		,"∈◎◎∋　　　＼∴￣＜《◎◎》＞￣∴／　　　∈◎◎∋\n"
		," ∥Θ∥　　　　 ＼　《◎≫≪◎》　／ 　　　　∥Θ∥\n"
		,"　＼∴＼　　　　　＼《◎≫≪◎》／　　　　　／∴／\n"
		,"　　＼∴＼＿＿＿＿／《◎≫≪◎》＼＿＿＿＿／∴／\n"
		,"　　　＼∴∴＿＿＿《◎≫　　≪◎》＿＿＿　∴／\n"
		,"　　　／∴／　　 ｜《◎≫　≪◎》｜ 　　＼∴＼\n"
		,"　　／∴／　　　 ｜《◎≫　≪◎》｜ 　　　＼∴＼\n"
		,"　／∴／　　／￣￣《◎≫　　≪◎》￣￣＼　　＼∴＼　　　　　　 ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		," ∥Θ∥ 　／　／￣＼《◎≫≪◎》／￣＼　＼　 ∥Θ∥　　　　　 ｜ $m1 ｜\n"
		,"∈◎◎∋ ∥Θ∥　　｜＜《◎》＞｜　　∥Θ∥ ∈◎◎∋　　 ▲　 ｜ $m2 ｜\n"
		,"＼＜＞／∈◎◎∋　 ｜＜《◎》＞｜ 　∈◎◎∋＼＜＞／　／＜＞＼｜ $m3 ｜\n"
		,"　 ▼　 ＼＜＞／　 ｜＜《◎》＞｜ 　＼＜＞／ 　▼　　 ∈◎◎∋｜ $m4 ｜\n"
		,"　　　　　 ▼　　　｜＜《◎》＞｜　　　▼　　　　　　　∥Θ∥＜  $m5 ｜\n"
		,"　　　　　　　　　　＼∴∴∴∴∴＼　　　　　　　　　　／∴／　｜ $m6 ｜\n"
		,"　　　　　　　　　　　＼∴∴∴∴∴＼＿＿＿＿＿＿＿＿／∴／　　｜ $m7 ｜\n"
		,"　　　　　　　　　　　　＼∴∴∴∴∴∴∴∴∴∴∴∴∴∴／　　　 ＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
		,"　　　　　　　　　　　　　￣￣￣￣￣￣￣￣￣￣￣￣￣￣\n"
)
}


sub pika009 {
push( @pikachiu, "       ,,,                              ,,,\n"
		,"       ,'',,,'',                        ,'',,,'',\n"
		,"     ,' ,'   ',;,,,,,,,'''''''''',,,,,,,;,'   ', ',\n"
		,"    ;  ;       ;;''    '',,  ,,''    '';;       ;  ;\n"
		,"   ;   ',    ,'            ''            ',    ,' ; ;\n"
		,"  ;  ,; ;;,,'  , , ;     ,,  ,,    ; ; ,  ',,;;   ;; ;\n"
		,"  ;  ;; ;;;   ;;;;;    ,'  ;'  ',   ;;;;;     ;;;  ; ;\n"
		," ;  ;'; ';   ; ' ;     ;        ;    ; ; '    ;'   ;  ;\n"
		," ;  '   ;     ,       ;          ;  ,          ;   ;  ;\n"
		," ;      ;  , ,;    ,  ;          ;, ;,   ,  ,  ;      ;\n"
		," ;      ,;;;,;',;,;',';          ;',';,:,';,';;,      ;\n"
		," ;     ; ;  ,,,,,,,,,,,,        ,,,,,,,,,,,,  ; ;     ;\n"
		," ;     ',;     ;      ;          ;      ;     ;,'     ;\n"
		," ;      ; ;     ',,,,'            ',,,,'     ; ;      ;   ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		," ;      ; ;                                  ; ;      ;  ｜ $m1 ｜\n"
		," ;      ;  ;   ////                 ////    ;  ;      ;  ｜ $m2 ｜\n"
		," ;   ,  ;   ;                              ;   ;  ,   ;  ｜ $m3 ｜\n"
		," ;   ;   ;   ;                            ;   ;   ;   ;  ｜ $m4 ｜\n"
		,"  ;  ;   ;   ;',         ,,,,,,         ,';   ;   ;  ;  ＜  $m5 ｜\n"
		,"   ;  ;   ;  ;  '',,                ,,''  ;  ;   ;  ;    ｜ $m6 ｜\n"
		,"    ;,; , ;   ;     ''''''''''''''''     ;   ; , ;,;     ｜ $m7 ｜\n"
		,"      ''''',;,;,                        ,;,;,'''''        ＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
)

}

sub pika010 {
push( @pikachiu, "\n"
		,"　　　　　　　　／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"　　　　　　　 ｜ $m1 ｜\n"
		,"　　　　　　　 ｜ $m2 ｜\n"
		,"　　　　　　　 ｜ $m3 ｜\n"
		,"　(○⌒`⌒ ○) ｜ $m4 ｜\n"
		,"／/ ( (( ))))＼｜ $m5 ｜\n"
		,"_/｛d ㊥ ㊥l ＼｜ $m6 ｜\n"
		,"/ ∧∧　〓ノ　＜  $m7 ｜\n"
		," (´ｰ`)y-~~＼　 ＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
)
}

sub pika011 {
push( @pikachiu, "\n"
		,"　　　　　　　　　　 ｜｜｜｜｜\n"
		,"　　　　　　　　　 ／￣￣￣￣￣＼\n"
		,"　　　　　　　　 ／　　　　　　　＼\n"
		,"　　　　　　　　│　　　　　　　　│\n"
		,"　　　　　　　　│　／　　　　＼　│　　／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"　　　　　　　／│　　━　　━　　│＼ ｜ $m1 ｜\n"
		,"　　　　　　 │ │　　　　　　　　│ │｜ $m2 ｜\n"
		,"　　　　　　　＼│　　　／＼　　　│／ ｜ $m3 ｜\n"
		,"　　　　　　　　│　　　￣￣　　　│　 ｜ $m4 ｜\n"
		,"　　　　　　　　│　　　　　　　　│　 ｜ $m5 ｜\n"
		,"　　　　　　　　│　　　～～　　　│　＜  $m6 ｜\n"
		,"　　　　　　　 ノ＼　　　￣　　　／ヽ　｜ $m7 ｜\n"
		,"　　　　　　　　 ノ＼＿＿＿＿＿／ヽ　　 ＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
		,"　　　　　　　　　＿｜　　　　｜＿\n"
		,"　　　　　　　／￣ ／　　　　　＼ ￣＼\n"
		,"　　　　　　／／￣￣￣￣￣￣￣￣￣￣＼＼\n"
		,"　　　　　／／　　　　　　　　　　　　＼＼\n"
		,"　　　　　| |　　　　　　　　　　　　　| |\n"
		,"　　　　／| | 　　　　　 ○ 　　　　　 | |＼\n"
		,"　　　／　| |　　　　　　　　　　　　　| |　＼\n"
		,"　　／　　| | 　　　　　　　　　　　　 | |　　＼\n"
		,"　／　　　| |　　　　　　　　　　　　　| |　　　＼\n"
		,"　|　　 ／| |　　　　　　○　　　　　　| |＼　　 |\n"
		,"　|　　 ＼| | 　　　　　　　　　　　　 | |／　　 |\n"
		,"　＼　　　| |　　　　　　　　　　　　　| |　　　／\n"
		,"　　＼　　| | 　　　　　　　　　　　　 | |　　／\n"
		,"　　　＼　| |　　　　　　○　　　　　　| |　／\n"
		,"　　　　＼| |　　　　　　　　　　　　　| |／\n"
		,"　　　　　| | 　　　　　　　　　　　　 | |\n"
		,"　　　　　| |　　　　　　　　　　　　　| |\n"
		,"　　　　　| | 　　　　　　　　　　　　 | |\n"
		,"　　　　　＼＼　　　　　　　　　　　　／／\n"
		,"　　　　　／＼＼____________________／／ ＼\n"
		,"　　　　／　　＼____________________／　　 ＼\n"
		,"　　　 |　　　／　　　　　　　　　 ＼　　　 |\n"
		,"　　　 |　　　|　　　　　　　　　　　|　　　|\n"
		,"　　　 |　　　|　　　　　　　　　　　|　　　|\n"
		,"　　　 |　　　|　　　　　　　　　　　|　　　|\n"
		,"　　　 |　　　|　　　　　　　　　　　|　　　|\n"
		,"　　 ／　　　 |　　　　　　　　　　　|　　　 ＼\n"
		,"　　 ￣￣￣￣￣　　　　　　　　　　　￣￣￣￣￣\n"
)
}

sub pika012 {

push( @pikachiu, "\n"
		," ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"｜ $m1 ｜\n"
		,"｜ $m2 ｜\n"
		,"｜ $m3 ｜\n"
		,"｜ $m4 ｜\n"
		,"｜ $m5 ｜\n"
		,"｜ $m6 ｜\n"
		,"｜ $m7 ｜\n"
		," ＼＿＿＿＿　＿＿＿＿＿＿＿／\n"
		,"　　　　　 ∨\n"
		," 　 　ヽ(´ー`)ノ\n"
		," 　　　 (　　 )\n"
		," 　　　 ノ 酔 ヽ\n"
		," 　　　　　拳 \n"
		," 　　　　　之 \n"
		," 　　　　　王 \n"

)
}

sub pika013 {

push( @pikachiu, "\n"
		,"　　　　　　　　　／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"　　γ　　 ヽ　　｜ $m1 ｜\n"
		,"　 ノ（((ｖ)）　 ｜ $m2 ｜\n"
		,"　（ ζσ σν　 ｜ $m3 ｜\n"
		,"　　 人\" - \"　　＜  $m4 ｜\n"
		," 　　　　　　　　｜ $m5 ｜\n"
		,"　　 ）　 （　　 ｜ $m6 ｜\n"
		,"　　＼　　 ／　　｜ $m7 ｜\n"
		," ＼　　(|)　　／　＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
		,"　 ＼ _)*(_ ／\n"
)
}
sub pika014 {

push( @pikachiu, "        　　＿＿\n"
		,"　　　　　 ｜  ｜\n"
		,"　　　　　Е＠＠ヨ\n"
		,"　　　　　 ｜曰｜\n"
		,"　　　　　＿ＴＴ＿\n"
		,"┌───ω────ω───┐\n"
		,"｜$m1｜\n"
		,"｜$m2｜\n"
		,"｜$m3｜\n"
		,"｜$m4｜\n"
		,"｜$m5｜\n"
		,"｜$m6｜\n"
		,"｜$m7｜\n"
		,"└────────────┘\n"

)
}

sub pika015 {

push( @pikachiu, "　　　　　　　　　　　　　　　　　　／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"　　　　　　　　　　　　　　　　　 ｜ $m1 ｜\n"
		,"　　　　　　　　　　　　　　　　　 ｜ $m2 ｜\n"
		,"　　　　　　　　　　　　　　　　　 ｜ $m3 ｜\n"
		,"　　　　　　　　　　　　　　　　　 ｜ $m4 ｜\n"
		,"　　　　　　　　　　　　　　　　　 ｜ $m5 ｜\n"
		,"　　　　　　　　　　　　　　　　　 ｜ $m6 ｜ _＿\n"
		,"　　　　　　　　　　　　　　　　　 ｜ $m7 ｜|　 |\n"
		,"　　　　　　　　　　　　　　　　　　＼＿＿＿＿＿＿＿＿　＿＿＿／ |　 |＼\n"
		,"　　　　　　　　　　　　　　　　　　　　　　　　　　　∨　　　　 |　 |＼＼\n"
		,"　　　　　　　　　　　　　　　　　　　　　　 ⌒(,-,)ヽ　　⊂＝＝⊃＝_|　＼＼\n"
		,"　　　　　　　　　　　　　　　　　　　　　　　　 ヽ(´π`) XXXXXX 　　　　＼＼\n"
		,"　　　　　　　　　　　　　　　　　　　　　　　　　　(　　)ヽXXXX　　　　　 ｜｜\n"
		,"　　　　　　　　　　　　　　　　　　　　　　　　　 ノ ωヽ  　　　　　　　 ｜｜\n"
		,"　　　　　　　　　　　　　　　　　　　　　　　　 彡　　　　　　　　　　　　｜｜\n"
		," ＿(´π`)_＿(´π`)_＿　　　　　　　 　　　　　 　　　　　　　　 　　　　 ｜｜\n"
		,"│ノ(　　)ヽノ(　　)ヽ│　　　　　　　　　　　　　 　 　　　　　　　　　　 ｜｜\n"
		,"∥￣ノ ωヽ￣ノ ωヽ￣∥ヽ(´π`)ノ　　　　　　　　　　　　　　　　　　　　｜｜\n"
		,"＿＿＿＿＿＿＿＿＿＿＿＿＿ (　　)＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿｜｜\n"
		,"￣￣￣￣￣￣￣￣￣￣￣￣￣ノ ωヽ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣｜｜\n"
)
}




sub pika016 {

push( @pikachiu, "　　　　　 ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"　　　　　｜ $m1 ｜\n"
		,"　　　　　｜ $m2 ｜\n"
		,"　　　　　｜ $m3 ｜\n"
		," 　┌-┐　｜ $m4 ｜\n"
		," 　┴-┴　｜ $m5 ｜\n"
		,"　 ´ﾑ｀　｜ $m6 ｜\n"
		,"　　/-ヽ ＜  $m7 ｜\n"
		,"   ＼V／ 　＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
		,"／│／  │＼┏ \n"
		,"━━━━━━╋━◇\n"
		,"  └┐┌┘  ┗\n"
		,"    ││\n"
		,"   ⊂  ⊃\n"
)
}

sub pika100 {

push( @pikachiu, "\n"
		,"　　　　　　　　　　　　　　 ／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"　　　　　　 ＿＿Д＿＿ 　　｜ $m1 ｜\n"
		,"　　　　　 ∠__,_λ_,__ヽ　 ｜ $m2 ｜\n"
		,"　　　　　　｜ ＠ .＠ ｜　　｜ $m3 ｜\n"
		,"　　　　　　 (“ ∇ ”)　　＜  $m4 ｜\n"
		,"　　　　　　 Λー─- Λ　　 ｜ $m5 ｜\n"
		,"　　　　　／~＼＼▼ ///ヽ　 ｜ $m6 ｜\n"
		,"　　　　／　　　３εヽ　 ＼ ｜ $m7 ｜\n"
		,"　　　 (　　／  V  V　＼　 ) ＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
		,"　　　　ゝ＿＿／=∞=＼＿_ノ　\n"
		," ＜＞　／　　　　/人　　　ヽ \n"
		,"　工　 ＼＿＿＿ノ/人ゝ＿＿／ \n"
		,"　□■□■□■□■□■□■□■□■\n"
)
}

sub pika101 {
push( @pikachiu, "\n" 
		,"　　　　　　　　　　／￣￣￣￣￣￣￣￣￣￣￣￣＼\n"
		,"　　　〃＼＼　　　 ｜ $m1 ｜\n"
		,"　 　 \@　 \@　　　　｜ $m2 ｜\n"
		," 〃/　　^ 　　ヽ 　｜ $m3 ｜\n"
		,"　　ヽ　~　 ノ　　＜  $m4 ｜\n"
		," /⌒　　　　 ⌒＼　｜ $m5 ｜\n"
		,"/　　　　　　　　＼｜ $m6 ｜\n"
		,"　|　・　　・　|　/｜ $m7 ｜\n"
		," /|　　　　　　| /　＼＿＿＿＿＿＿＿＿＿＿＿＿／\n"
		,"　|　　 .　　　|　 \n"
		,"　|　　　　　　|　\n"
		,"　|　　　　　　|\n"
		,"　|　＼ ∥ ／　|\n"
		,"　|　　 ||　　 |\n"
		,"　|　　 ||　　 |\n"
		,"　|_____||_____|\n"
		,"　|　　 || ∽　|\n"
)
}

sub regist {
	# 別のページからこのＣＧＩへの投稿を排除する処理
	&error(1) unless($ENV{'HTTP_REFERER'} =~/$cgiurl/);

	if (!open(TIME,"$timefile")) { &error(0); }
	$prevtime = <TIME>;
	close(TIME);
	&error(3) if ($prevtime > time - $interval);


	@msgs = split(/\r/,$MSG{'value'});

	foreach (0 .. $maxrow - 1) {
		$msgs[$_] =~ s/\s/ /g;
		$len = length($msgs[$_]);
		$msgs[$_] = substr( "$msgs[$_]                        ", 0, 24);

		$msgs[$_] =~ s/</&lt\;/g;

	}
	if (!open(DB,"$file")) { &error(0); }
	@lines = <DB>;
	close(DB);
	if(@lines > $max-1) { pop(@lines); }
	srand;

	#出現率の設定
	#出現率を変えたいときはrand(xx)の値を変える。

	#すげー手抜き

	$random = 0;
	$rnd = int rand(20);
	$random = 1 if ($rnd == 0);
	$rnd = int rand(25);
	$random = 2 if ($rnd == 0);
	$rnd = int rand(30);
	$random = 3 if ($rnd == 0);
	$rnd = int rand(40);
	$random = 4 if ($rnd == 0);
	$rnd = int rand(55);
	$random = 5 if ($rnd == 0);
	$rnd = int rand(70);
	$random = 6 if ($rnd == 0);
	$rnd = int rand(80);
	$random = 7 if ($rnd == 0);
	$rnd = int rand(100);
	$random = 8 if ($rnd == 0);
	$rnd = int rand(115);
	$random = 9 if ($rnd == 0);
	$rnd = int rand(125);
	$random = 10 if ($rnd == 0);
	$rnd = int rand(130);
	$random = 11 if ($rnd == 0);
	$rnd = int rand(140);
	$random = 12 if ($rnd == 0);
	$rnd = int rand(200);
	$random = 13 if ($rnd == 0);
	$rnd = int rand(200);
	$random = 14 if ($rnd == 0);
	$rnd = int rand(200);
	$random = 15 if ($rnd == 0);
	$rnd = int rand(200);
	$random = 16 if ($rnd == 0);
	$rnd = int rand(200);
	$random = 17 if ($rnd == 0);

	if ( $MSG{'value'} =~ /おじゃる/ ) { $random = 100; }
	if ( $MSG{'value'} =~ /さくらのマンコ/ ) { $random = 101; }
	$random = $MSG{'face'} if ( $MSG{'face'} > 0 );
	$m1 = $msgs[0];
	$m2 = $msgs[1];
	$m3 = $msgs[2];
	$m4 = $msgs[3];
	$m5 = $msgs[4];
	$m6 = $msgs[5];
	$m7 = $msgs[6];

	&getpika;

	#過去ログ自動作成
	if (!open(LOG,">>$filedate")) { &error(2); }
	if (-z $filedate) {
#		print LOG "<html><title>$title Log $month/$mday</title>\n";
		print LOG "<html><title>$title Log $month</title>\n";
		print LOG "$body\n";
#		print LOG "<h2 align=center>$title Log $month/$mday</h2>\n";
		print LOG "<h2 align=center>$title Log $month</h2>\n";


		print LOG "<pre>\n";
	}

	print LOG "$border投稿日：$date\n";
	print LOG @pikachiu;
	close(LOG);

	$value = "$date\t$msgs[0]\t$msgs[1]\t$msgs[2]\t$msgs[3]\t$msgs[4]\t$msgs[5]\t$msgs[6]\t$random\t\n";
	unshift( @lines,$value);
	if (!open(DB,">$file")) { &error(0); }
	print DB @lines;
	close(DB);

	if (!open(TIME,">$timefile")) { &error(0); }
	print TIME time;
	close(TIME);

	print "Location: $cgiurl" . "?bgcolor=$bgc\&textcolor=$textc\&def=$def\&fontsize=$fontsize" . "\n\n";
	exit;
}

sub getpika {
	if ( $random < 2 ) { &normal; }
	elsif ( $random == 2 ) { &pika001; }
	elsif ( $random == 3 ) { &pika002; }
	elsif ( $random == 4 ) { &pika003; }
	elsif ( $random == 5 ) { &pika004; } 
	elsif ( $random == 6 ) { &pika005; }
	elsif ( $random == 7 ) { &pika006; }
	elsif ( $random == 8 ) { &pika007; }
	elsif ( $random == 9 ) { &pika008; }
	elsif ( $random == 10 ) { &pika009; }
	elsif ( $random == 11 ) { &pika010; }
	elsif ( $random == 12 ) { &pika011; }
	elsif ( $random == 13 ) { &pika012; }
	elsif ( $random == 14 ) { &pika013; }
	elsif ( $random == 15 ) { &pika014; }
	elsif ( $random == 16 ) { &pika015; }
	elsif ( $random == 17 ) { &pika016; }
	elsif ( $random == 100 ) { &pika100; }
	elsif ( $random == 101 ) { &pika101; }
	elsif ( $random == 200 ) { &normal2; }
	elsif ( $random == 201 ) { &normal3; }
	else { &normal; }
}


sub error {

	$error = $_[0];
	if    ($error == 0) { $errmsg = 'An error occurred in the input/output of the recording file.'; }
	elsif ($error == 1) { $errmsg = "URL of post screen is <br>$cgiurl<br>" . 'Submissions cannot be made from other than'; }
	elsif ($error == 2) { $errmsg = "Could not open log file."; }
	elsif ($error == 3) { $errmsg = "Posting interval too short. Please wait $interval seconds."; }

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
	print "<h1>$errmsg</h1>\n";
	print "</body></html>\n";
	exit;
}

sub counter {

	for( $i=0 ; $i < $countlevel ; $i++){
		open(IN,"$countfile$i$countfiledat");
		$count[$i] = <IN>;
		$filenumber[$count[$i]] = $i;
		close(IN);
	}
	@sortedcount = sort {$a <=> $b;} @count;
	$maxcount = $sortedcount[$countlevel-1];
	$mincount = $sortedcount[0];

	$maxcount++;
	
	#きりのいい数字になった時の処理
	#面倒くさいのでif文の羅列

	if ($maxcount % 100000 == 0) { print "<font size=7>$maxcount</font> "; }
	elsif ($maxcount % 10000 == 0) { print "<font size=6>$maxcount</font> "; }
	elsif ($maxcount % 1000 == 0) { print "<font size=5>$maxcount</font> "; }
	elsif ($maxcount % 100 == 0) { print "<font size=4>$maxcount</font> "; }
	elsif (substr("000000$maxcount", -6) % 111111 == 0) { print "<font size=7>$maxcount</font> "; }
	elsif (substr("00000$maxcount", -5) % 11111 == 0) { print "<font size=6>$maxcount</font> "; }
	elsif (substr("0000$maxcount", -4) % 1111 == 0) { print "<font size=5>$maxcount</font> "; }
	else { print "$maxcount "; }

	open(OUT,">$countfile$filenumber[$mincount]$countfiledat");
	print OUT $maxcount;
	close(OUT);

	open(DAY, $daycount);
	$data = <DAY>;
	close(DAY);
	($c_date, $yesterday, $today, $win, $mac, $other_os, $ie, $nn) = split(/<>/, $data);

	if ($ENV{'HTTP_USER_AGENT'} =~ /Win/) { $win++; }
	elsif ($ENV{'HTTP_USER_AGENT'} =~ /Mac/) { $mac++; }
	else {$other_os++;}
	if ($ENV{'HTTP_USER_AGENT'} =~ /MSIE/) { $ie++; }
	else {$nn++;}

	if ($c_date ne "$month$mday") {
		$c_date = "$month$mday";
		$yesterday = $today;
		$today = 0;
		# カウンタのログ。アクセスがあった日の最初のアクセス時間と、その時点でのカウント数を記録する
		# あんまり意味が無いようなのでコメントアウトした
		# &error(2) if (!open(COUNTLOG,">>./countlog.txt"));
		# print COUNTLOG "$month/$mday $hour:$min:$sec [$maxcount]";
		# close(COUNTLOG);
	}
	$today++;
	open(DAY, ">$daycount");
	print DAY "$c_date<>$yesterday<>$today<>$win<>$mac<>$other_os<>$ie<>$nn";
	close(DAY);

	print "（Today：$today Yesterday：$yesterday ｜ Win：$win Mac：$mac Other：$other_os ｜ IE：$ie Netscape Navigator (etc.)：$nn ）<br>";
}


#end_of_script
