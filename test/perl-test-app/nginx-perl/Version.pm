package Version;

use nginx;

sub installed {
  return "$^V";
}

sub handler {
  my $r = shift;
  $r->send_http_header("text/html");
  $r->print("Perl location handler is working");
  return OK;
}

1;
__END__
