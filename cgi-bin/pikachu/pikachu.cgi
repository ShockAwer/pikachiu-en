#! /usr/local/bin/perl
#���̓T�[�o�ɂ���ĈႤ�̂œK�X�ύX�̎�

# SunechamaBBS Ver2.20 �҂�����d�l�{ShibaCounter+1.943

# �J����
# AN HTTP Server 1.21c + Perl for Win32 Ver5.00307 + Cygwin Perl Ver5.00562 + Netscape Navigator 4.08(����m�F�Ɏg�p)



#�f�t�H���g�̐ݒ�Ŏg���ꍇ(shin����̃c���[�\���p�N��܂����Bshin���񂲂߂�)
#	|--------- [cgi-bin]�i755�j
#			|
#			|-- countlog.txt (666)�i�J�E���^�̃��O�t�@�C���B�f�t�H���g�̐ݒ�ł͕K�v�����j
#			|-- getdir.cgi (755)�i�f�B���N�g�����X�g�\���X�N���v�g�B�f�B���N�g�����X�g���\���o���Ȃ��T�[�o(Virtualave��)�p�j
#			|-- jcode.pl (755)�i���{��R�[�h�ϊ����C�u�����j
#			|-- pikachu.cgi (755)�i���̃X�N���v�g�j
#			|-- pikachu.log (666)�i�L�^�t�@�C���j
#			|-- time.txt (666)�i���e���ԋL�^�t�@�C���B�A�����e��h�~����̂Ɏg�p�j
#			|
#			|--[count](777)
#			|    |
#			|    |--count?.txt(666)�i�A�N�Z�X�J�E���^�t�@�C���B count0�`$countlevel-1.txt��u���B�j
#			|    |--day.txt(666)�i����̃A�N�Z�X����OS��u���E�U�ʂ̃J�E���^�t�@�C���B���b�N������~���[�����O�͈�؂��ĂȂ��̂ŉ��₷���j
#			|
#			|--[log](755)���O�t�@�C���ۑ��f�B���N�g��
#			     |
#			     |--�N��.html(666)�������͔N����.html(666)(�ߋ����O�t�@�C��)
#			     |			���Ƃ���1999�N12���Ȃ�A�N=1999 ��=12�A�܂�199912.html��u���B
#			     |			��t�@�C���ł����B
#			     |			log�f�B���N�g���̃p�[�~�b�V������7x7���ƃt�@�C����u���Ȃ��Ă������I�ɍ쐬����݂����B






$title = '���₵�����҂�����';

# body��
$bgc    = '004040';
$textc  = 'ffffff';
$linkc  = 'eeffee';
$vlinkc = 'dddddd';
$alinkc = 'ff0000';

# �\������
$def = 30;

# �ő�ۑ�����
$max = 300;

$fontsize = 2;

# ���� gmtime�֐�������{���Ԃ𓾂Ă���̂ŁA���e���Ԃ���{���ԈȊO�ɂ���������
# �T�[�o�̓������v������Ă鎞�ȊO��0�ł����B
$tim = 0;

#�ő�s��
$maxrow = 7;

# -------------------------------------------- �J�E���^ --------------------------------------------
# �J�E���^�̋��x
$countlevel = 2;
$countfile = './count/count';
$countfiledat = '.txt';
$countdate = '99/04/20';

$daycount = './count/day.txt';



# ���̃X�N���v�g �P�� $cgiurl = 'pikachu.cgi'; �ł��������A�t���p�X����ꂽ�ق�����������
$cgiurl = 'pikachu.cgi';

#�T�|�[�g�f����URL�@�����ꍇ�͋󗓁i $supporturl = ''; �j�ɂ���B
$supporturl = 'http://8616.teacup.com/gmama/bbs';


# �Ǘ��l�̃��[���A�h���X�@�����ꍇ�͋󗓁i $mailadd = ''; �j�ɂ���B
$mailadd = 'webmaster@nelii.ducub.com';

# ------------------------------------ �f�B���N�g���E�t�@�C���� ------------------------------------
# ���{��R�[�h�ϊ����C�u����jocde.pl�̃p�X
# ��i��̃f�B���N�g���ɒu���ꍇ�� require '../jcode.pl'; �ɂ���
require '../jcodeLE.pl';

# ���e���������܂��L�^�t�@�C���̃p�X��ݒ�
$file = './pikachu.log';

# �ʓr�Ƃ郍�O�̕ۑ���f�B���N�g���E�t�@�C�����擪�����E�g���q�̎w��
$logdir ='../../pikachulog/';
$logfile = ''; # $logfile = 'pikachu' 
$logfiledat = '.html';

#�ŋ߂̉ߋ����O�̏ꏊ
#getdir.cgi���g��Ȃ��ꍇ�� $logpath = $logdir; �ɂ���
$logpath = './getdir.cgi';



#���O�t�@�C���̌r��
# $border = "--------------------------------------------------------------------------------\n";
$border = '<hr>';


# ���e���ԋL�^�t�@�C���̃p�X
$timefile = './time.txt';
# �A�����e�������ԁi�b�j
# �K�v��������0�ɂ���
$interval = 60;


# ���͌`���̐ݒ�
$method = 'post';

$action = 'thunder';

# ��������
($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = gmtime(time+32400+$tim);
$month++;

$youbi = ('��','��','��','��','��','��','�y') [$wday];
$month = "0$month" if ($month < 10);
$mday = "0$mday" if ($mday < 10);
$hour = "0$hour" if ($hour < 10);
$min = "0$min" if ($min < 10);
$sec = "0$sec" if ($sec < 10);

$year += 1900;

# �����t�H�[�}�b�g
$date = "$month��$mday��($youbi)$hour��$min��$sec�b";

# ���O�t�@�C�����擾
# �������݂������Ƃ��� $filedate = "$logdir$logfile$year$month$mday$logfiledat"; �ɂ���
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


#	�o�i�\�͂�����print "</body></html>\n";�̈�s��ɏ���

#	print "<!--#echo banner=\"\"-->";

	print "<hr>\n";

	print "<font size=+1><b>$title</b></font>\n";
	print "<font size=-1><b><a href=\"mailto:$mailadd\">�A����</a> " if ($mailadd ne '');
	print "<a href=\"$supporturl\">�T�|�[�g�f����</a>" if ($supporturl ne '');

	print "</b></font>\n";
	&printform;
	if ( $countlevel > 0 ){
		print "$countdate���� ";
		&counter;
	}
	print "<hr>\n";
	print '<table border="0" cellpadding="1" cellspacing="0" width="99%"><tr bgcolor="#004040"><td>';
	print "\n<a href=\"http://dauso.virtualave.net/cgi-bin/bbs.cgi\">���₵�����҂�����</a>�b\n";
	print "<a href=\"http://www.org1.com/~osamu/pbbs.cgi\">�҂����イ�����C�\\<font size=-1><sup>TM</sup></font></a><p>\n";
	print "<font color=white>�ŋ߂̉ߋ����O��</font><a href=\"./$logpath\">����</a></td></tr></table>\n";



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

		print "<hr>���e���F$date\n";

		&getpika;
		print @pikachiu;
		splice( @pikachiu, 0);

	}

	$p_next = $p_end + 1;
	$s = $page + 1;
	$e = $p_end + 1;
	$linecount++;
	if ($end < 0) { print"<hr>�L���͂���܂���"; }
	else { print "<hr>�V���� $s�`$e�i�L�^����$linecount �ő�L�^���� $max�j</pre><p>\n"; }
	if ($p_end ne ($linecount - 1)) {
		print "<form method=$method action=\"$cgiurl\">\n";
		print "<input type=hidden name=\"page\" value=\"$p_next\">\n";
		print "<input type=hidden name=\"def\" value=\"$def\">\n";
		print "<input type=hidden name=\"bgcolor\" value=\"$bgc\">\n";
		print "<input type=hidden name=\"textcolor\" value=\"$textc\">\n";
		print "<input type=hidden name=\"fontsize\" value=\"$fontsize\">\n";
		print "<input type=submit value=\"���̃y�[�W\"></form>\n";
	}
	print "<h4 align=right><a href=\"http://www.geocities.com/Tokyo/Dojo/5886/cgi/index.html\">SunechamaBBS</a> Ver2.30 �҂�����d�l�{ShibaCounter+1.943</h4>\n";
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
	print "<html><head><title>�\\���m�F</title></head>\n";
	print "$body\n";
	print "<pre>";
	print "�����������͂�������\n";
	print "----------------------------------------\n";
	print $MSG{'value'};
	print "\n----------------------------------------\n";
	print "\n\n<pre>���ۂɕ\\������镶��\n";
	print " �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n";
	print "�b $msgs[0] �b\n";
	print "�b $msgs[1] �b\n";
	print "�b $msgs[2] �b\n";
	print "�b $msgs[3] �b\n";
	print "�b $msgs[4] �b\n";
	print "�b $msgs[5] �b\n";
	print "�b $msgs[6] �b\n";
	print " �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^</pre>\n";
	print "<form method=$method action=\"$cgiurl\">\n";
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "<textarea name=\"value\" rows=7 cols=24>$MSG{'value'}</textarea><br>\n";
	print "<input type=hidden name=face value=$MSG{'face'}>";
	print "�\\������\n";
	print "<input type=text name=\"def\" size=3 value=\"$def\" maxlength=3>\n";
	print "BG�J���[\n";
	print "<input type=text name=\"bgcolor\" size=6 value=\"$bgc\">\n";
	print "Text�J���[\n";
	print "<input type=text name=\"textcolor\" size=6 value=\"$textc\">\n";
	print "font size\n";
	print "<input type=text name=\"fontsize\" size=2 value=\"$fontsize\" maxlength=1><br>\n";
	print "<input type=submit value=\"���e\"><input type=reset value=\"����\"><p>\n";

	print "</form></body></html>\n";
	exit;
}

sub printform {
	print "<form method=$method action=\"$cgiurl\">\n";
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "<table><tr><td>\n";
	print "<textarea name=\"value\" rows=7 cols=24></textarea></td>\n";
	print "<td valign=bottom><pre>\n";
	print " �@�@ /|�@ /|\n";
	print "�@�@ / |�@/ |\n";
	print "�@�@/�@�܁@�@\n";
	print "�� /��_�@���@\n";
	print "�@(�Z �`�@�Z </pre></td>";
	print "<td valign=bottom><pre>�@�@�@�@ �@�@�@��\n";
	print "�@�@�@���@�@�@�@�@��\n";
	print "�@�@�@�_�_�Q�Q�Q�^�^\n";
	print "�@�^�_ /�@�@�@�@ �_ \n";
	print "�@�_�@�b�@���@�D���b\n";
	print "�@�@�_�b���@�@�`�@��\n";
	print "�@�@�^�����@�@�@�@��\n";
	print "�@�@�_���@�@�@�@�@�b\n";
	print "�@�@�@�b�Q�Z�Q�Q�Q�Z\n";
	print "</pre></td>\n";
	print "<td valign=bottom><pre>";
	print "�@���_�Q�Q_�^���@�Q�Q\n";
	print "�@ �_�@�@�@ �^ �^�@�^\n";
	print "��  /��� �� �_ �_�@�_\n";
	print "�@�i�j �`�@�� �_/�@�^\n";
	print "</pre></td></tr>\n";
	print "<tr><td><input type=checkbox name=confirm value=checked checked>�\\���m�F</td>\n";
	print "<td align=center><input type=radio name=face value=0 checked></td>\n";
	print "<td align=center><input type=radio name=face value=200></td>\n";
	print "<td align=center><input type=radio name=face value=201></td>\n";
	print "</tr></table>\n";
	print "���p24�����i�S�p��12�����j�~�V�s�܂łł��B����ȏ�͐؂�̂Ă��܂��B<p>\n";
	print "�\\������\n";
	print "<input type=text name=\"def\" size=3 value=\"$def\" maxlength=3>\n";
	print "BG�J���[\n";
	print "<input type=text name=\"bgcolor\" size=6 value=\"$bgc\">\n";
	print "Text�J���[\n";
	print "<input type=text name=\"textcolor\" size=6 value=\"$textc\">\n";
	print "font size\n";
	print "<input type=text name=\"fontsize\" size=2 value=\"$fontsize\" maxlength=1>\n";
	print "<a href=\"$cgiurl?bgcolor=$bgc\&textcolor=$textc\&def=$def\&fontsize=$fontsize\">Bookmark</a><br>\n";
	print "�Œ�s�b�`�t�H���g�𐳂����ݒ肵�Ă������ꍇ�́A����<b>font size</b>�����낢��ς��Č��Ă�������<p>\n";
	print "<input type=submit value=\"���e�^�����[�h\"><input type=reset value=\"����\"><p>\n";
	print "</form>\n";

}


sub normal {

	if ($random == 0 ) { $eye = "��_�@��"; }
	else { $eye = "��_�@�� �߶�"; }

	push( @pikachiu, "\n"
			," �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
			,"�b $m1 �b\n"
			,"�b $m2 �b\n"
			,"�b $m3 �b\n"
			,"�b $m4 �b�@�@ /|�@ /|\n"
			,"�b $m5 �b �@ / |�@/ |\n"
			,"�b $m6 �b�@ /�@�܁@�@\n"
			,"�b $m7  �� /$eye \n"
			," �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^�@(�Z �`�@�Z\n"
	)
}

sub normal2 {


	push( @pikachiu, "\n"

			," �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
			,"�b $m1 �b\n"
			,"�b $m2 �b\n"
			,"�b $m3 �b\n"
			,"�b $m4 �b\n"
			,"�b $m5 �b\n"
			,"�b $m6 �b\n"
			,"�b $m7 �b\n"
			," �_�Q�Q�Q�Q�Q�Q�@�Q�Q�Q�Q�Q�^\n"
			,"�@�@�@�@ �@�@�@��\n"
			,"�@�@�@���@�@�@�@�@��\n"
			,"�@�@�@�_�_�Q�Q�Q�^�^\n"
			,"�@�^�_ /�@�@�@�@ �_\n"
			,"�@�_�@�b�@���@�D���b\n"
			,"�@�@�_�b���@�@�`�@��\n"
			,"�@�@�^�����@�@�@�@��\n"
			,"�@�@�_���@�@�@�@�@�b\n"
			,"�@�@�@�b�Q�Z�Q�Q�Q�Z\n"
	)
}



sub normal3 {


	push( @pikachiu, "\n"

		," �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�b $m1 �b\n"
		,"�b $m2 �b\n"
		,"�b $m3 �b\n"
		,"�b $m4 �b\n"
		,"�b $m5 �b���_�Q�Q_�^���@�Q�Q\n"
		,"�b $m6 �b �_�@�@�@ �^ �^�@�^\n"
		,"�b $m7  �� /��� �� �_ �_�@�_\n"
		," �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^ �i�j �`�@�� �_/�@�^\n"
	)
}


sub pika001 {
push( @pikachiu, "\n"
		," �^�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�b$m1�b\n"
		,"�b$m2�b\n"
		,"�b$m3�b\n"
		,"�b$m4 �� ����\n"
		,"�b$m5�b�@�i�@�R\n"
		,"�b$m6�b�@�@�_&lt;&lt;�j\n"
		,"�b$m7�b�@�@�@�b�@�_\n"
		," �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^ �@�@�@��\n"
)
}

sub pika002 {

push( @pikachiu, "����������������������������������������������������������������������\n"
		,"���h�b�p�����h�b�p�����h�b�p�����h�b�p�����h�b�p�����h�b�p�����h�b�p��\n"
		,"����������������������������������������������������������������������\n"
		,"�����������@�@ �^�P�P�P�P�P�P�P�P�P�P�P�P�_�@�@�@�@�@�@�@�@ ����������\n"
		,"���h�b�p���@�@�b $m1 �b�@�@�@�@�@�@�@�@���h�b�p��\n"
		,"�����������@�@�b $m2 �b�@�@�@�@�@�@�@�@����������\n"
		,"�����������@�@�b $m3 �b�@�@�@�@�@�@�@�@����������\n"
		,"���h�b�p���@�@�b $m4 �b�@�@ /|�@ /|�@�@���h�b�p��\n"
		,"�����������@�@�b $m5 �b �@ / |�@/ |�@�@����������\n"
		,"�����������@�@�b $m6 �b�@ /�@�܁@�@�@�@����������\n"
		,"���h�b�p���@�@�b $m7�@�� /�� �@���G�@�@���h�b�p��\n"
		,"�����������@�@ �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^�@(�Z �D�@�Z�@�@ ����������\n"
		,"����������������������������������������������������������������������\n"
		,"���h�b�p�����h�b�p�����h�b�p�����h�b�p�����h�b�p�����h�b�p�����h�b�p��\n"
		,"����������������������������������������������������������������������\n"
)
}

sub pika003 {

push( @pikachiu, "\n"
		,"�@�@�@�@�@�@�@�@ �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�@�@�@�@�@�@�@�@�b $m1 �b\n"
		,"�@�@�@�@�@�@�@�@�b $m2 �b\n"
		,"�@�@�@�@�@�@�@�@�b $m3 �b\n"
		,"�@�@�@�@�@�@�@�@�b $m4 �b\n"
		,"�@�@�@�@�@�@�@�@�b $m5 �b\n"
		,"�@�@�@�@ �� �ȁ@�b $m6 �b\n"
		,"�`���P�P(�L�[`)��  $m7 �b\n"
		,"  UU�P�P U  U�@�@�_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
)
}

sub pika004 {

push( @pikachiu, " �@�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q\n"
		," �^�@�@�@�@�@�@�@�@�@�@�@�@�_\n"
		,"�b $m1 �b\n"
		,"�b $m2 �b\n"
		,"�b $m3 �b\n"
		,"�b $m4 �b\n"
		,"�b $m5 �b\n"
		,"�b $m6 �b\n"
		,"�b $m7 �b\n"
		," �_�Q�Q�Q�Q�@�Q�Q�Q�Q�Q�Q�Q�^\n"
		,"�@�@�@�@�@ ��\n"
		,"�@�` �R(�L�D`)�m �����Ձ`��\n"
		,"�@�` �@�i�@�@�j�@�`\n"
		,"�@�` �@�m �ցR�@ �`\n"
)
}

sub pika005 {

push( @pikachiu, " �@�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q\n"
		," �^�@�@�@�@�@�@�@�@�@�@�@�@�_\n"
		,"�b $m1 �b\n"
		,"�b $m2 �b\n"
		,"�b $m3 �b�@�@ ��\n"
		,"�b $m4 �b�@�^�����_\n"
		,"�b $m5 �b�@��������\n"
		,"�b $m6  ���@�a���a\n"
		,"�b $m7 �b�@�@�_���_\n"
		," �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^�@�@�@ �_���_\n"
)
}

sub pika006 {
push( @pikachiu, "�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�b�b�b�b�b\n"
		," �@�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�@�@�@�@ �^�P�P�P�P�P�_\n"
		," �^�@�@�@�@�@�@�@�@�@�@�@�@�_�@�@ �^�@�@�@�@�@�@�@�_\n"
		,"�b $m1 �b�@ ���@�^�@�@�@�@�_�@��\n"
		,"�b $m2 �b �^���@�@���@�@���@�@���_\n"
		,"�b $m3 �b�� ���@�@�@�����@�@�@�� ��\n"
		,"�b $m4 �b �_���@�@�@�����@�@�@���^\n"
		,"�b $m5 �b�@ ���@�@�i�@�@�j�@�@��\n"
		,"�b $m6 �b�@ ���@�@ �Q�Q�Q �@�@��\n"
		,"�b $m7  ���@���@�@ �_�Q�^�@�@ ��\n"
		," �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^ �@�m�_�@�@�@�@�@�@�@�^�R\n"
		,"�@ �@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �m�_�Q�Q�Q�Q�Q�^�R\n"
)
}

sub pika007 {


push( @pikachiu, "\n"
		," �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�b $m1 �b\n"
		,"�b $m2 �b\n"
		,"�b $m3 �b\n"
		,"�b $m4 �b\n"
		,"�b $m5 �b\n"
		,"�b $m6 �b\n"
		,"�b $m7 �b\n"
		," �_�Q�Q�Q�Q�Q�Q�@�Q�Q�Q�Q�Q�^\n"
		," �@�@�@�@�@�@�@��\n"
		,"�@�@�@ �^�P�_�Q�Q�Q�^�P�_\n"
		,"�@�@ �^ �^�_�@�q�r�@�^�_ �_\n"
		,"�@�@�b�^ �@�b���@���b�@ �_�b\n"
		,"�@�@�b�v�v��� �� �߁�v�v�b\n"
		,"�@�@�b �^ �i�P�P�P�P�j �_ �b\n"
		,"�@�@ �v�@ �^||�v�v||�_�@ �v\n"
		,"�@�@�@�@ �b �Y�@�@�Y �b\n"
		,"�@ �^�P�P�P�@�@�ȁ@�@�P�P�P�_\n"
		," �@�P�P�P�P�P�P�@�P�P�P�P�P�P\n"
)
}

sub pika008 {

push( @pikachiu, "�@�@�@�@�@�@�@�@ ���@�@�@�@�@�@�@��\n"
		,"�@�@�@�@�@�@�@�^�����_�@ �� �@�^�����_\n"
		,"�@�@�@�@�@�@�@���������^�����_��������\n"
		,"�@�@�@�@�@�@ ���a���a �������� �a���a��\n"
		,"�@�@�@�@�@�^�����_�@ ���a���a�� �@�^�����_\n"
		,"�@�@�@�@�@���������^�����_�^�����_��������\n"
		,"�@�@�@�@ ���a���a ���������������� �a���a��\n"
		,"�@�@�@�^�����_ �@���a���a�@�a���a���@ �^�����_\n"
		,"�@�@�@���������^�����_�@ �� �@�^�����_��������\n"
		,"�@�@�@ �a���a ���������^�����_�������� �a���a\n"
		,"�@�@�@�@�_���_ �a���a �������� �a���a �^���^\n"
		,"�@ ���@�@ �_���_�_���_ �a���a �^���^�^���^ �@�@��\n"
		,"�^�����_�@�@�_���_�_���P�s�t�P���^�^���^�@�@�^�����_\n"
		,"���������@�@�@�_���P���s�����t���P���^�@�@�@��������\n"
		," �a���a�@�@�@�@ �_�@�s����ၝ�t�@�^ �@�@�@�@�a���a\n"
		,"�@�_���_�@�@�@�@�@�_�s����ၝ�t�^�@�@�@�@�@�^���^\n"
		,"�@�@�_���_�Q�Q�Q�Q�^�s����ၝ�t�_�Q�Q�Q�Q�^���^\n"
		,"�@�@�@�_�����Q�Q�Q�s����@�@�ၝ�t�Q�Q�Q�@���^\n"
		,"�@�@�@�^���^�@�@ �b�s����@�ၝ�t�b �@�@�_���_\n"
		,"�@�@�^���^�@�@�@ �b�s����@�ၝ�t�b �@�@�@�_���_\n"
		,"�@�^���^�@�@�^�P�P�s����@�@�ၝ�t�P�P�_�@�@�_���_�@�@�@�@�@�@ �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		," �a���a �@�^�@�^�P�_�s����ၝ�t�^�P�_�@�_�@ �a���a�@�@�@�@�@ �b $m1 �b\n"
		,"�������� �a���a�@�@�b���s���t���b�@�@�a���a ���������@�@ ���@ �b $m2 �b\n"
		,"�_�����^���������@ �b���s���t���b �@���������_�����^�@�^�����_�b $m3 �b\n"
		,"�@ ���@ �_�����^�@ �b���s���t���b �@�_�����^ �@���@�@ ���������b $m4 �b\n"
		,"�@�@�@�@�@ ���@�@�@�b���s���t���b�@�@�@���@�@�@�@�@�@�@�a���a��  $m5 �b\n"
		,"�@�@�@�@�@�@�@�@�@�@�_�����������_�@�@�@�@�@�@�@�@�@�@�^���^�@�b $m6 �b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�_�����������_�Q�Q�Q�Q�Q�Q�Q�Q�^���^�@�@�b $m7 �b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�_�����������������������������^�@�@�@ �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�P�P�P�P�P�P�P�P�P�P�P�P�P�P\n"
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
		," ;      ; ;     ',,,,'            ',,,,'     ; ;      ;   �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		," ;      ; ;                                  ; ;      ;  �b $m1 �b\n"
		," ;      ;  ;   ////                 ////    ;  ;      ;  �b $m2 �b\n"
		," ;   ,  ;   ;                              ;   ;  ,   ;  �b $m3 �b\n"
		," ;   ;   ;   ;                            ;   ;   ;   ;  �b $m4 �b\n"
		,"  ;  ;   ;   ;',         ,,,,,,         ,';   ;   ;  ;  ��  $m5 �b\n"
		,"   ;  ;   ;  ;  '',,                ,,''  ;  ;   ;  ;    �b $m6 �b\n"
		,"    ;,; , ;   ;     ''''''''''''''''     ;   ; , ;,;     �b $m7 �b\n"
		,"      ''''',;,;,                        ,;,;,'''''        �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
)

}

sub pika010 {
push( @pikachiu, "\n"
		,"�@�@�@�@�@�@�@�@�^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�@�@�@�@�@�@�@ �b $m1 �b\n"
		,"�@�@�@�@�@�@�@ �b $m2 �b\n"
		,"�@�@�@�@�@�@�@ �b $m3 �b\n"
		,"�@(����`�� ��) �b $m4 �b\n"
		,"�^/ ( (( ))))�_�b $m5 �b\n"
		,"_/�od �� ��l �_�b $m6 �b\n"
		,"/ �ȁȁ@���m�@��  $m7 �b\n"
		," (�L�`)y-~~�_�@ �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
)
}

sub pika011 {
push( @pikachiu, "\n"
		,"�@�@�@�@�@�@�@�@�@�@ �b�b�b�b�b\n"
		,"�@�@�@�@�@�@�@�@�@ �^�P�P�P�P�P�_\n"
		,"�@�@�@�@�@�@�@�@ �^�@�@�@�@�@�@�@�_\n"
		,"�@�@�@�@�@�@�@�@���@�@�@�@�@�@�@�@��\n"
		,"�@�@�@�@�@�@�@�@���@�^�@�@�@�@�_�@���@�@�^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�@�@�@�@�@�@�@�^���@�@���@�@���@�@���_ �b $m1 �b\n"
		,"�@�@�@�@�@�@ �� ���@�@�@�@�@�@�@�@�� ���b $m2 �b\n"
		,"�@�@�@�@�@�@�@�_���@�@�@�^�_�@�@�@���^ �b $m3 �b\n"
		,"�@�@�@�@�@�@�@�@���@�@�@�P�P�@�@�@���@ �b $m4 �b\n"
		,"�@�@�@�@�@�@�@�@���@�@�@�@�@�@�@�@���@ �b $m5 �b\n"
		,"�@�@�@�@�@�@�@�@���@�@�@�`�`�@�@�@���@��  $m6 �b\n"
		,"�@�@�@�@�@�@�@ �m�_�@�@�@�P�@�@�@�^�R�@�b $m7 �b\n"
		,"�@�@�@�@�@�@�@�@ �m�_�Q�Q�Q�Q�Q�^�R�@�@ �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
		,"�@�@�@�@�@�@�@�@�@�Q�b�@�@�@�@�b�Q\n"
		,"�@�@�@�@�@�@�@�^�P �^�@�@�@�@�@�_ �P�_\n"
		,"�@�@�@�@�@�@�^�^�P�P�P�P�P�P�P�P�P�P�_�_\n"
		,"�@�@�@�@�@�^�^�@�@�@�@�@�@�@�@�@�@�@�@�_�_\n"
		,"�@�@�@�@�@| |�@�@�@�@�@�@�@�@�@�@�@�@�@| |\n"
		,"�@�@�@�@�^| | �@�@�@�@�@ �� �@�@�@�@�@ | |�_\n"
		,"�@�@�@�^�@| |�@�@�@�@�@�@�@�@�@�@�@�@�@| |�@�_\n"
		,"�@�@�^�@�@| | �@�@�@�@�@�@�@�@�@�@�@�@ | |�@�@�_\n"
		,"�@�^�@�@�@| |�@�@�@�@�@�@�@�@�@�@�@�@�@| |�@�@�@�_\n"
		,"�@|�@�@ �^| |�@�@�@�@�@�@���@�@�@�@�@�@| |�_�@�@ |\n"
		,"�@|�@�@ �_| | �@�@�@�@�@�@�@�@�@�@�@�@ | |�^�@�@ |\n"
		,"�@�_�@�@�@| |�@�@�@�@�@�@�@�@�@�@�@�@�@| |�@�@�@�^\n"
		,"�@�@�_�@�@| | �@�@�@�@�@�@�@�@�@�@�@�@ | |�@�@�^\n"
		,"�@�@�@�_�@| |�@�@�@�@�@�@���@�@�@�@�@�@| |�@�^\n"
		,"�@�@�@�@�_| |�@�@�@�@�@�@�@�@�@�@�@�@�@| |�^\n"
		,"�@�@�@�@�@| | �@�@�@�@�@�@�@�@�@�@�@�@ | |\n"
		,"�@�@�@�@�@| |�@�@�@�@�@�@�@�@�@�@�@�@�@| |\n"
		,"�@�@�@�@�@| | �@�@�@�@�@�@�@�@�@�@�@�@ | |\n"
		,"�@�@�@�@�@�_�_�@�@�@�@�@�@�@�@�@�@�@�@�^�^\n"
		,"�@�@�@�@�@�^�_�_____________________�^�^ �_\n"
		,"�@�@�@�@�^�@�@�_____________________�^�@�@ �_\n"
		,"�@�@�@ |�@�@�@�^�@�@�@�@�@�@�@�@�@ �_�@�@�@ |\n"
		,"�@�@�@ |�@�@�@|�@�@�@�@�@�@�@�@�@�@�@|�@�@�@|\n"
		,"�@�@�@ |�@�@�@|�@�@�@�@�@�@�@�@�@�@�@|�@�@�@|\n"
		,"�@�@�@ |�@�@�@|�@�@�@�@�@�@�@�@�@�@�@|�@�@�@|\n"
		,"�@�@�@ |�@�@�@|�@�@�@�@�@�@�@�@�@�@�@|�@�@�@|\n"
		,"�@�@ �^�@�@�@ |�@�@�@�@�@�@�@�@�@�@�@|�@�@�@ �_\n"
		,"�@�@ �P�P�P�P�P�@�@�@�@�@�@�@�@�@�@�@�P�P�P�P�P\n"
)
}

sub pika012 {

push( @pikachiu, "\n"
		," �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�b $m1 �b\n"
		,"�b $m2 �b\n"
		,"�b $m3 �b\n"
		,"�b $m4 �b\n"
		,"�b $m5 �b\n"
		,"�b $m6 �b\n"
		,"�b $m7 �b\n"
		," �_�Q�Q�Q�Q�@�Q�Q�Q�Q�Q�Q�Q�^\n"
		,"�@�@�@�@�@ ��\n"
		," �@ �@�R(�L�[`)�m\n"
		," �@�@�@ (�@�@ )\n"
		," �@�@�@ �m �� �R\n"
		," �@�@�@�@�@�� \n"
		," �@�@�@�@�@�V \n"
		," �@�@�@�@�@�� \n"

)
}

sub pika013 {

push( @pikachiu, "\n"
		,"�@�@�@�@�@�@�@�@�@�^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�@�@���@�@ �R�@�@�b $m1 �b\n"
		,"�@ �m�i((��)�j�@ �b $m2 �b\n"
		,"�@�i �ă� �Ѓˁ@ �b $m3 �b\n"
		,"�@�@ �l\" - \"�@�@��  $m4 �b\n"
		," �@�@�@�@�@�@�@�@�b $m5 �b\n"
		,"�@�@ �j�@ �i�@�@ �b $m6 �b\n"
		,"�@�@�_�@�@ �^�@�@�b $m7 �b\n"
		," �_�@�@(|)�@�@�^�@�_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
		,"�@ �_ _)*(_ �^\n"
)
}
sub pika014 {

push( @pikachiu, "        �@�@�Q�Q\n"
		,"�@�@�@�@�@ �b  �b\n"
		,"�@�@�@�@�@�E������\n"
		,"�@�@�@�@�@ �b�H�b\n"
		,"�@�@�@�@�@�Q�s�s�Q\n"
		,"���������ք��������ք�������\n"
		,"�b$m1�b\n"
		,"�b$m2�b\n"
		,"�b$m3�b\n"
		,"�b$m4�b\n"
		,"�b$m5�b\n"
		,"�b$m6�b\n"
		,"�b$m7�b\n"
		,"����������������������������\n"

)
}

sub pika015 {

push( @pikachiu, "�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �b $m1 �b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �b $m2 �b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �b $m3 �b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �b $m4 �b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �b $m5 �b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �b $m6 �b _�Q\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �b $m7 �b|�@ |\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�_�Q�Q�Q�Q�Q�Q�Q�Q�@�Q�Q�Q�^ |�@ |�_\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�Ɂ@�@�@�@ |�@ |�_�_\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ ��(,-,)�R�@�@����������_|�@�_�_\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �R(�L��`) XXXXXX �@�@�@�@�_�_\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@(�@�@)�RXXXX�@�@�@�@�@ �b�b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �m �ցR  �@�@�@�@�@�@�@ �b�b\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �c�@�@�@�@�@�@�@�@�@�@�@�@�b�b\n"
		," �Q(�L��`)_�Q(�L��`)_�Q�@�@�@�@�@�@�@ �@�@�@�@�@ �@�@�@�@�@�@�@�@ �@�@�@�@ �b�b\n"
		,"���m(�@�@)�R�m(�@�@)�R���@�@�@�@�@�@�@�@�@�@�@�@�@ �@ �@�@�@�@�@�@�@�@�@�@ �b�b\n"
		,"�a�P�m �ցR�P�m �ցR�P�a�R(�L��`)�m�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�@�b�b\n"
		,"�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q (�@�@)�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�b�b\n"
		,"�P�P�P�P�P�P�P�P�P�P�P�P�P�m �ցR�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�P�b�b\n"
)
}




sub pika016 {

push( @pikachiu, "�@�@�@�@�@ �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�@�@�@�@�@�b $m1 �b\n"
		,"�@�@�@�@�@�b $m2 �b\n"
		,"�@�@�@�@�@�b $m3 �b\n"
		," �@��-���@�b $m4 �b\n"
		," �@��-���@�b $m5 �b\n"
		,"�@ �LсM�@�b $m6 �b\n"
		,"�@�@/-�R ��  $m7 �b\n"
		,"   �_V�^ �@�_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
		,"�^���^  ���_�� \n"
		,"������������������\n"
		,"  ��������  ��\n"
		,"    ����\n"
		,"   ��  ��\n"
)
}

sub pika100 {

push( @pikachiu, "\n"
		,"�@�@�@�@�@�@�@�@�@�@�@�@�@�@ �^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�@�@�@�@�@�@ �Q�Q�D�Q�Q �@�@�b $m1 �b\n"
		,"�@�@�@�@�@ ��__,_��_,__�R�@ �b $m2 �b\n"
		,"�@�@�@�@�@�@�b �� .�� �b�@�@�b $m3 �b\n"
		,"�@�@�@�@�@�@ (�g �� �h)�@�@��  $m4 �b\n"
		,"�@�@�@�@�@�@ ���[��- ���@�@ �b $m5 �b\n"
		,"�@�@�@�@�@�^~�_�_�� ///�R�@ �b $m6 �b\n"
		,"�@�@�@�@�^�@�@�@�R�ÁR�@ �_ �b $m7 �b\n"
		,"�@�@�@ (�@�@�^  V  V�@�_�@ ) �_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
		,"�@�@�@�@�T�Q�Q�^=��=�_�Q_�m�@\n"
		," �����@�^�@�@�@�@/�l�@�@�@�R \n"
		,"�@�H�@ �_�Q�Q�Q�m/�l�T�Q�Q�^ \n"
		,"�@��������������������������������\n"
)
}

sub pika101 {
push( @pikachiu, "\n" 
		,"�@�@�@�@�@�@�@�@�@�@�^�P�P�P�P�P�P�P�P�P�P�P�P�_\n"
		,"�@�@�@�V�_�_�@�@�@ �b $m1 �b\n"
		,"�@ �@ \@�@ \@�@�@�@�@�b $m2 �b\n"
		," �V/�@�@^ �@�@�R �@�b $m3 �b\n"
		,"�@�@�R�@~�@ �m�@�@��  $m4 �b\n"
		," /�܁@�@�@�@ �܁_�@�b $m5 �b\n"
		,"/�@�@�@�@�@�@�@�@�_�b $m6 �b\n"
		,"�@|�@�E�@�@�E�@|�@/�b $m7 �b\n"
		," /|�@�@�@�@�@�@| /�@�_�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�^\n"
		,"�@|�@�@ .�@�@�@|�@ \n"
		,"�@|�@�@�@�@�@�@|�@\n"
		,"�@|�@�@�@�@�@�@|\n"
		,"�@|�@�_ �a �^�@|\n"
		,"�@|�@�@ ||�@�@ |\n"
		,"�@|�@�@ ||�@�@ |\n"
		,"�@|_____||_____|\n"
		,"�@|�@�@ || ��@|\n"
)
}

sub regist {
	# �ʂ̃y�[�W���炱�̂b�f�h�ւ̓��e��r�����鏈��
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

	#�o�����̐ݒ�
	#�o������ς������Ƃ���rand(xx)�̒l��ς���B

	#�����[�蔲��

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

	if ( $MSG{'value'} =~ /�������/ ) { $random = 100; }
	if ( $MSG{'value'} =~ /������̃}���R/ ) { $random = 101; }
	$random = $MSG{'face'} if ( $MSG{'face'} > 0 );
	$m1 = $msgs[0];
	$m2 = $msgs[1];
	$m3 = $msgs[2];
	$m4 = $msgs[3];
	$m5 = $msgs[4];
	$m6 = $msgs[5];
	$m7 = $msgs[6];

	&getpika;

	#�ߋ����O�����쐬
	if (!open(LOG,">>$filedate")) { &error(2); }
	if (-z $filedate) {
#		print LOG "<html><title>$title�ߋ����O $month��$mday��</title>\n";
		print LOG "<html><title>$title�ߋ����O $month��</title>\n";
		print LOG "$body\n";
#		print LOG "<h2 align=center>$title�ߋ����O $month��$mday��</h2>\n";
		print LOG "<h2 align=center>$title�ߋ����O $month��</h2>\n";


		print LOG "<pre>\n";
	}

	print LOG "$border���e���F$date\n";
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
	
	#����̂��������ɂȂ������̏���
	#�ʓ|�������̂�if���̗���

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
		# �J�E���^�̃��O�B�A�N�Z�X�����������̍ŏ��̃A�N�Z�X���ԂƁA���̎��_�ł̃J�E���g�����L�^����
		# ����܂�Ӗ��������悤�Ȃ̂ŃR�����g�A�E�g����
		# &error(2) if (!open(COUNTLOG,">>./countlog.txt"));
		# print COUNTLOG "$month/$mday $hour:$min:$sec [$maxcount]";
		# close(COUNTLOG);
	}
	$today++;
	open(DAY, ">$daycount");
	print DAY "$c_date<>$yesterday<>$today<>$win<>$mac<>$other_os<>$ie<>$nn";
	close(DAY);

	print "�i�����F$today ����F$yesterday �b Win�F$win Mac�F$mac Other�F$other_os �b IE�F$ie NN���F$nn �j<br>";
}


#end_of_script