#!/usr/bin/perl -w

# Written by Diwei Chen
# First edit: 21/10/2016
# Last edit:  29/10/2016

# This program is implementing a simple online social media.
 
use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;


sub main() {
    # print start of HTML ASAP to assist debugging if there is an error in the script
    print page_header();
    
    # Now tell CGI::Carp to embed any warning in HTML
    warningsToBrowser(1);

    # define some global variables
    $debug = 1;
    $users_dir = "dataset-medium";
    
    print user_page();
    print page_trailer();
}


#
# Show unformatted details for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {
	
	my $flag = param('flag') || "";
	# check if a user has logined
	my $flag_login = param('flag_login');
	# print "$flag";
    my $n = param('n') || 0;
	my $p = param('p') || 0;
	my $mate_id = param('mate_id') || 0;
	if (defined $p) {
		$p = 0 if $p < 0;
	}
    my @users = sort(glob("$users_dir/*"));
	my $user_to_show;
	#matelook
	# search
	my $search = param('search');
	
	# get current user's id
	my $zid = param('flag_login');
	# get content of new post
	my $newpost = param('newpost');
	
	# get comment contents
	my $comment = param('comment');
	if (defined $comment) {
		# dataset-medium/z3275760/posts/22/comments
		my $path = param('path_to_update');
		# make dir if the dir does not exist
		mkdir "$path" if ! -e "$path";
		my $comment_path = "$path/*";
		my @comments_dir = grep {-d} glob $comment_path;
		my $new_comment_count = (scalar @comments_dir) + 1;
		
		my $new_comment_path = "$path/$new_comment_count";
		mkdir "$new_comment_path";
		my $new_comment_txt = "$new_comment_path/comment.txt";
		open FILE, ">> $new_comment_txt";
		
		# the following 3 lines of code got from https://www.tutorialspoint.com/perl/perl_date_time.htm
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
		$year += 1900;
		$mon += 1;
		my $time = "$year"."-"."$mon"."-"."$mday"."T"."$hout"."$min"."$sec"."+0000";
		
		my $comment_content = <<eof;
time=$time
from=$zid
message=$comment
eof
		print FILE $comment_content;
		close FILE;
		
	}
	
	# get reply contents
	my $reply = param('reply');
	if (defined $reply) {
		my $path = param('path_to_update');
		mkdir "$path" if ! -e "$path";
		my $replies_path = "$path/*";
		my @replies_dir = grep {-d} glob $replies_path;
		my $new_replies_count = (scalar @replies_dir) + 1;
		
		my $new_reply_path = "$path/$new_replies_count";
		mkdir "$new_reply_path";
		my $new_reply_txt = "$new_reply_path/reply.txt";
		open FILE, ">> $new_reply_txt";
		
		# the following 3 lines of code got from https://www.tutorialspoint.com/perl/perl_date_time.htm
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
		$year += 1900;
		$mon += 1;
		my $time = "$year"."-"."$mon"."-"."$mday"."T"."$hout"."$min"."$sec"."+0000";
		
		my $reply_content = <<eof;
time=$time
from=$zid
message=$reply
eof

		print FILE $reply_content;
		close FILE;
	}
	
	if (defined $newpost && defined $zid) {

		my $posts_path = "$users_dir/$zid/posts/*";

		my @posts_dir = grep {-d} glob $posts_path;

		my $post_name = scalar @posts_dir;
		my $path_newpost_dir = "$users_dir/$zid/posts/$post_name";
		mkdir "$path_newpost_dir";
		my $path_newpost_txt = $path_newpost_dir . "/post.txt";
		# the following 3 lines of code got from https://www.tutorialspoint.com/perl/perl_date_time.htm
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
		$year += 1900;
		$mon += 1;
		
		my $time = "$year"."-"."$mon"."-"."$mday"."T"."$hout"."$min"."$sec"."+0000";
		my $post_content = <<eof;
time=$time
from=$zid
message=$newpost	
eof
		open FILE , ">> $path_newpost_txt"; 
		print FILE $post_content;
		close FILE;
	}
	
	my $searchpost = param('searchpost');
	if (defined $searchpost) {
		my $return_contents;
		my $path = "$users_dir/*";
		my @users_dir = grep {-d} glob $path;
		my $matched_post;
		my $flag_find = 0;
		foreach my $u (@users_dir) {

			my $path_post = "$u/posts/*";
			my @posts_dir = grep {-d} glob $path_post;
			foreach my $p (@posts_dir) {
				my $path_post_txt = "$p/post.txt";
				open my $file, "$path_post_txt" if -e "$path_post_txt";
				my $post_contents = join('', <$file>);
				my $post_contents_lc = lc $post_contents;
				my $searchpost_lc = lc $searchpost;
				# find matched post
				if (index($post_contents_lc, $searchpost_lc) != -1) {
					$flag_find = 1;
					my $path_to_update = "$p/comments";			
					my $post = <<eof;
					<div class="matelook_post_details">
					<h4>Post: </h4>
eof
					$post .= $post_contents;
					$post .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="hidden" name="path_to_update" value="$path_to_update">
<input type="text" name="comment" class="col-xs-6">   <input type="submit" class="btn btn-info" value="Comment">
</form>				
</div>
eof
					$matched_post .= $post;
					$return_contents .= $post;
				}
				close $file;
			}
		}
		if ($flag_find == 0) {
			$return_contents .= "No Results.";
		}
		$return_contents .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="submit" value="Go Back" class="matelook_button">
</form>	
eof
		
		return $return_contents;
	}
	elsif (defined $search) {
		# table header
		my $html_search_results = "<table style='width:100%'><tr>";

		# iterate through users dir		
		foreach my $user_to_show (@users) {
			my $details_path = "$user_to_show" . "/user.txt";
			open my $file, "$details_path" or die "can not open $details_path: $!";
			my $details = join('', <$file>);
			# name
			my $name;
			if ($details =~ /(full_name=.*?\n)/) {
				$name = $1;
				$name =~ s/full_name=//;
				chomp $name;
			}
			# zid
			my $zid;
			if ($details =~ /(zid=.*?\n)/) {
				$zid = $1;
				$zid =~ s/zid=//;
				$zid =~ s/\s+$//;
			}

			my $name_lc = lc $name;
			my $search_lc = lc $search;
			if (index($name_lc, $search_lc) != -1) {
				# find matched name
				my $link_image = $user_to_show . "/profile.jpg";
				my $html_tmp = <<eof;
				<tr>
				<form method="POST" action="">
				<input type="hidden" name="mate_id" value="$zid">
				<input type="hidden" name="flag" value="id">
				<input type="hidden" name="flag_login" value="$zid">
				<input type="image" src="$link_image" alt="img" style="height:40px; width:40px">
				<input type="submit" value="$name" class="matelook_button">
				</form>
				</tr>
eof
			
				$html_search_results = $html_search_results . $html_tmp;
			}
			close($file); 
		}

		# table tailer
		$html_search_results = $html_search_results . "</tr></table>";
		
		return $html_search_results;
	}
	elsif (defined $flag_login) {
		# check pre or next button clicked
		if ($flag eq 'pre') {
		$user_to_show  = $users[$p % @users];

		}
		elsif ($flag eq 'next') {
			$user_to_show  = $users[$n % @users];
		}
		elsif ($flag eq 'id') {
			$user_to_show = "$users_dir/"."$mate_id";
		}
		else {
			$user_to_show  = $users[0];
		}
		# print "$user_to_show";
    	my $details_filename = "$user_to_show/user.txt";
    	open my $file, "$details_filename" or die "can not open $details_filename: $!";
    	my $details = join '', <$file>;
    	close $file;
	
		# print profile image
		my $profile_filename = "$user_to_show/profile.jpg";
		$profile_filename = $profile_filename if -e $profile_filename;

		# try to display a universal profile
		if ($profile_filename == 0) {
			#$profile_filename = "all.gif";
		}

		# full name
		my $name;
		if ($details =~ /(full_name=.*?\n)/) {
			$name = $1;
			$name =~ s/full_name=//;
			chomp $name;
		}

		# zid
		my $zid;
		if ($details =~ /(zid=.*?\n)/) {
			$zid = $1;
			$zid =~ s/zid=//;
			$zid =~ s/\s+$//;
		}

		# birthday
		my $birthday;
		if ($details =~ /(birthday=.*?\n)/) {
			$birthday = $1;
			$birthday =~ s/birthday=//;
		}

		# program
		my $program;
		if ($details =~ /(program=.*?\n)/) {
			$program = $1;
			$program =~ s/program=//;
		}

		# mates
		my $mates;
		if ($details =~ /(mates=.*?\n)/) {
			$mates = $1;
			$mates =~ s/mates=//;
		}
		my @mates_list;
		# match each mate 
		while ($mates =~ /(z\d+)/g) {
			# initialise mates_list
			push(@mates_list, $1);
		}
		my $html_mates;
		# header of table
		
		
		$html_mates = "<table style='width:100%'><tr>";
		foreach my $mate (@mates_list) {
			my $link_image = "$users_dir/" . "$mate/" . "profile.jpg";
			# get the name of the mate
			my $path = "$users_dir/$mate/user.txt";
			open $file, "$path" if -e "$path";
			my $content = join('', <$file>);
			my $name;
			if ($content =~ /(name=[a-zA-Z ]*)/) {
				$name = $1;
				chomp $name;
				$name =~ s/name=//;
			}
			
			$html_tmp = <<eof;
			<tr style="width:10%">
			<form method="POST" action="">
			<input type="hidden" name="mate_id" value="$mate">
			<input type="hidden" name="flag" value="id">
			<input type="hidden" name="flag_login" value="true">
			<input type="image" src="$link_image" alt="img" style="height:40px; width:40px">
			<input type="submit" value="$name" class="matelook_button">
			</form>
			</tr>
eof
			$html_mates = $html_mates . $html_tmp;
		}
		# tailer of table	
		$html_mates = $html_mates . "</tr></table>";
		# home_suburb
		my $home_suburb;
		if ($details =~ /(home_suburb=.*?\n)/) {
			$home_suburb;
			$home_suburb =~ s/home_suburb=//;
		}

		# posts dir of current user
		my @posts_details_cur;
		my $posts_path = "$user_to_show/posts/*";
		my @posts_dir = grep { -d } glob $posts_path;
		# save posts of current user
		foreach my $p (@posts_dir) {
			my $path = $p . "/post.txt";
			open my $f, "$path" if -e "$path";
			my $post = join('', <$f>);
			
			my @post_contents = split("\n", $post);
			my $tag;
			
			# find the row of time
			for(my $i = 0; $i < scalar @post_contents; $i += 1) {
				if ($post_contents[$i] =~ /time=/) {
					$tag = $i;			
				}
			}
			my $tmp_time = <<eof;
<div class="matelook_post_details">
<h4>Post: </h4>
eof
			$tmp_time .= $post_contents[$tag];
			$tmp_time =~ s/^\s+//;
	
			splice(@post_contents, $tag, 1);
			unshift(@post_contents, $tmp_time);
			$post = join("\n", @post_contents);
			#$post = $post . "\n\n";
			
			my $path_to_update = "$p/comments";
			$post .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="hidden" name="path_to_update" value="$path_to_update">
<input type="text" name="comment" class="col-xs-6">   <input type="submit" class="btn btn-info" value="Comment">
</form>
eof

			# add comments to the post
			my $comments_path = "$p/comments/*";
			my @comments_dir = grep {-d} glob $comments_path;
			foreach my $c (@comments_dir) {
				my $path = "$c/comment.txt";
				open my $f, $path if -e $path;
				my $comment = <<eof;
<div class="matelook_post_details_comment">		
eof
				$comment .= "<h5>Comment: </h5>";
				$comment .= join('', <$f>);
				my $path_to_update = "$c/replies";
				$comment .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="hidden" name="path_to_update" value="$path_to_update">
<input type="text" name="reply" class="col-xs-6">   <input type="submit" class="btn btn-primary" value="Reply">
</form>
eof
				$post .= $comment;
				close $f;
				
				#add replies to the comment
				my $replies_path = "$c/replies/*";
				my @replies_dir = grep {-d} glob $replies_path;
				foreach my $r (@replies_dir) {
				
					my $path = "$r/reply.txt";
					open my $f, $path if -e $path;
					my $reply = <<eof;
					<div class="matelook_post_details_reply">		
eof
					$reply .= "<h5>Reply: </h5>";
					$reply .= join('', <$f>);
					$reply .= <<eof;
					</div>
eof
					$post .= $reply;
					close $f;
				}
				$post .= <<eof;
</div>
eof
			} 
			$post .= <<eof;
</div>
eof
			
			push(@posts_details_cur, $post);
			@posts_details_cur = reverse sort @posts_details_cur;
			close $f;
		}

		# zid lists to exclude
		my @exclude_zid;
		push(@exclude_zid, $zid);
		
		# posts dir of mates_list
		my @posts_details_mates;
		foreach my $mate (@mates_list) {
			push(@exclude_zid, $mate);
			my $path = "$users_dir/$mate/posts/*";
			my @posts_dir = grep { -d } glob $path;
			# find each post 
			foreach my $p (@posts_dir) {
				my $path = $p . "/post.txt";
				open my $f, $path if -e $path;
				my $post = <<eof;
				<div class="matelook_post_details_mate">
				<h4>Post(from mates): </h4>
eof
				$post .= join('', <$f>);
				# add gap line to each post
				$post .= "\n\n";
				# save each post of this mate
				my $path_to_update = "$p/comments";
				$post .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="hidden" name="path_to_update" value="$path_to_update">
<input type="text" name="comment" class="col-xs-6">   <input type="submit" class="btn btn-info" value="Comment">
</form>
eof
				
				my $path_dir_comment = "$p/comments/*";
				my @comments_dir = grep {-d} glob $path_dir_comment;
				# find each comment
				foreach my $p (@comments_dir) {
					my $path = $p . "/comment.txt";
					open my $f, $path if -e $path;
					
					my $comment = <<eof;
					<div class="matelook_post_details_comment">
					<h5>Comment: </h5>
eof
					$comment .= join('', <$f>);
					my $path_to_update = "$p/replies";
					$comment .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="hidden" name="path_to_update" value="$path_to_update">
<input type="text" name="reply" class="col-xs-6">   <input type="submit" class="btn btn-primary" value="Reply">
</form>
eof
					$post .= $comment;
					
					
					my $path_dir_replies = "$p/replies/*";
					my @replies_dir = grep {-d} glob $path_dir_replies;
					# find each reply
					foreach my $r (@replies_dir) {
						my $path = $r . "/reply.txt";
						open my $f, $path if -r $path;
						my $reply = <<eof;
						<div class="matelook_post_details_reply">		
eof
						$reply .= "<h5>Reply: </h5>";
						$reply .= join('', <$f>);
						$reply .= <<eof;
						</div>
eof
						$post .= $reply;
						close $f;
					}
					
					$post .= <<eof;
</div>
eof
				}
				$post .= <<eof;
</div>
eof
				push(@posts_details_mates, $post);
				close $f;
			}
		}
		
		# find posts that contain current user's zid
		my @posts_details_find;
		my $path_users = "$users_dir/*";
		my @users = grep {-d} glob $path_users;
		# time complexity n^3
		foreach my $user_dir (@users) {
			my $uid = $1 if $user_dir =~ /(z\d+)/;
			# if this uid is not in the excluded id list
			if (!grep(/$uid/, @exclude_zid)) {
				my $path = "$user_dir/posts/*";
				my @posts_dir = grep {-d} glob $path;
				# find posts that contain zid
				foreach my $p (@posts_dir) {
					my $path_post = $p . "/post.txt";
					open my $f, $path_post if -e $path_post;
					my $post = <<eof;
<div class="matelook_post_details">
Post(containing zid):
eof
					$post .= join('', <$f>);
					# print $path;
					# print $post;
					# print $zid;
					
					if ($post =~ /$zid/g) {
						$post .= "\n\n";
						my $path_to_update = "$p/comments";
						$post .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="hidden" name="path_to_update" value="$path_to_update">
<input type="text" name="comment" class="col-xs-6">   <input type="submit" class="btn btn-info" value="Comment">
</form>
</div>
eof
						push(@posts_details_find, $post);
					}
					else {
						my $path_dir_comments = "$p/comments/*";
						my @comments_dir = grep {-d} glob $path_dir_comments;
						# find comments that contain zid
						my $flag_contain = 0;
						foreach my $c (@comments_dir) {
							my $path_comment = "$c/comment.txt";
							open my $f, $path_comment if -e $path_comment;
							my $comment = join('', <$f>);
							if ($comment =~ /$zid/) {
								$flag_contain = 1;
								my $path_to_update = "$p/comments";
								$post .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="hidden" name="path_to_update" value="$path_to_update">
<input type="text" name="comment" class="col-xs-6">   <input type="submit" class="btn btn-info" value="Comment">
</form>
eof
								
								$post .= "\n\n";
								
								last;
							}
							else {
								my $path_dir_replies = "$c/replies/*";
								my @replies_dir = grep {-d} glob $path_dir_replies;
								# find replies that contain zid
								foreach my $r (@replies_dir) {
									my $path_reply = "$r/reply.txt";
									open my $f, $path_reply if -e $path_reply;
									my $reply = join('', <$f>);
									if ($reply =~ /$zid/) {
										$flag_contain = 1;
										my $path_to_update = "$p/comments";
										$post .= <<eof;
<form method="POST" action="">
<input type="hidden" name="flag_login" value="$zid">
<input type="hidden" name="path_to_update" value="$path_to_update">
<input type="text" name="comment" class="col-xs-6">   <input type="submit" class="btn btn-info" value="Comment">
</form>
eof
										$post .= "\n\n";
									}
									close $f;
								}							
							}
							close $f;
						}
						if ($flag_contain == 1) {
							$post .= <<eof;
</div>						
eof
							push(@posts_details_find, $post);
						}
					}
					close $f;
				}
			}
		}
		#print @users;
		
   		my $next_user = $n + 1;
		my $pre_user = $n - 1;
		
    	return <<eof;
<form method="POST" action="">
	<input type="text" name="search">
	<input type="submit" value="Search Users" class="matelook_button">
</form>
<form method="POST" action="">
	<input type="text" name="searchpost">
	<input type="submit" value="Search Posts" class="matelook_button">
</form>
<form method="POST" action="">
	<input type="hidden" name="flag_login" value="$zid">
	<input type="text" name="newpost">
	<input type="submit" value="Post" class="matelook_button">
</form>
<img src="$profile_filename" alt="">

<form method="POST" action="">
	<input type="hidden" name="p" value="$pre_user">
	<input type="hidden" name="flag" value="pre">
	<input type="hidden" name="flag_login" value="$zid">
	<input type="submit" value="Pre user" class="matelook_button">
</form>
<p>
<form method="POST" action="">
    <input type="hidden" name="n" value="$next_user">
	<input type="hidden" name="flag" value="next">
	<input type="hidden" name="flag_login" value="$zid">
    <input type="submit" value="Next user" class="matelook_button">
</form>
<form method="POST" action="">
	<input type="submit" value="Logout" class="matelook_button">
</form>

<div class="matelook_user_details">
	<h4>User's Information:</h4>
	<div class="matelook_user_details">
	Full Name: $name
	</div>
	<div class="matelook_user_details">
	Student ID: $zid
	</div>
	<div class="matelook_user_details">
	Mates: $html_mates
	</div>
	<div class="matelook_user_details">
	Birthday: $birthday
	</div>
	<div class="matelook_user_details">
	Program: $program
	</div>
</div>
@posts_details_cur

@posts_details_mates


<div class="matelook_post_details">
@posts_details_find
</div>

eof
		
	}
	# display login page
	else {	
		my $html_login;
		my $username = param('username') || "";
		my $u_password = param('password') || "";
		my $flag_jump = -1;
		foreach my $user_to_show (@users) {
			# get user
			my $details_path = "$user_to_show" . "/user.txt";
			open my $file, "$details_path" or die "can not open $details_path: $!";
			my $details = join('', <$file>);
			# zid
			my $zid;
			if ($details =~ /(zid=.*?\n)/) {
				$zid = $1;
				$zid =~ s/zid=//;
				$zid =~ s/\s+$//;
			}
			# password
			my $password;
			if ($details =~ /(password=.*?\n)/) {
				$password = $1;
				$password =~ s/password=//;
				$password =~ s/\s+$//;
			}
			if ($username eq $zid && $u_password eq $password) {
				$flag_jump = 1;
				last;
			}
		}
		
		if ($flag_jump == -1) {
			$html_login = <<eof;
<div class="container">
<form method="POST" action="">
	<h3>Please use a user ID and password stored in the database to login.</h3>
	<div class="form_group">
		<label for="usr"> User ID(zid): </label>
	</div>
	<input type="text" name="username" class="form_control input-lg" id="usr">
	<div class="form_group">
		<label for="pwd">Password: </label>
	</div>
	<input type="password" name="password" class="form_control input-lg" id="pwd">
	<div class="form_group">
		<input type="submit" name="Login" value="Login" class="btn btn-info">
	</div>
	
</form>
</div>
eof
		}
		elsif ($flag_jump == 1) {
			$html_login = <<eof;
<form id="mk" method="POST" action="">
<input type="hidden" name="flag_login" value="true">
</form>
<script type="text/javascript" language="JavaScript">
document.getElementById("mk").submit();
</script>
eof
		}

		return $html_login;
	}
	
}


#
# HTML placed at the top of every page
#
sub page_header {
    return <<eof
Content-Type: text/html;charset=utf-8

<!DOCTYPE html>
<html lang="en">
<head>
<title>DateWay</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

<link href="matelook.css" rel="stylesheet">
</head>
<body>
<div class="matelook_heading">
DateWay
</div>
eof
}


#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}

main();
