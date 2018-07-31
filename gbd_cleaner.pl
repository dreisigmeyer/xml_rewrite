use strict;
use warnings;

use lib 'PerlModules';
use HtmlEntities;
use File::Path qw(make_path remove_tree);

=begin
Cleans up the HTML that may be in the patent data XML files.
1) Converts HTML entities to UTF8 encodings
=end
=cut

# Helper functions
sub decToHex {
   return '\u' . sprintf "%04X", $_[0]
}

sub entToHex {
   my %htmlEntities;
   exists $htmlEntities{$_[0]} ? $htmlEntities{$_[0]} : '&' . $_[0] . ';'
}

sub padHex {
   return '\u' . uc sprintf "%04s", $_[0]
}

sub process02to04 {
    my ($XML_FILE_NAME) = @_;
    # The 2002-2004 XML files reference external image files which aren't there
    `sed -i -r 's_(<!ENTITY.*NDATA.*>)_<!--\\1-->_g' $XML_FILE_NAME`;
    `sed -i -r 's_(<EMI.*FILE.*>)_<!--\\1-->_g' $XML_FILE_NAME`;
    `sed -i -r 's_(<CHEMCDX.*FILE.*>)_<!--\\1-->_g' $XML_FILE_NAME`;
    `sed -i -r 's_(<CHEMMOL.*FILE.*>)_<!--\\1-->_g' $XML_FILE_NAME`;
    # And other crap
    `sed -i -r 's_(<MATHEMATICA.*>)_<!--\\1-->_g' $XML_FILE_NAME`;
    `sed -i -r 's_(<CUSTOM-CHARACTER FILE[^>]*>)_<!--\\1-->_g' $XML_FILE_NAME`;
}

my $fileName=$ARGV[0];
my $outFileName = $fileName . ".cleaned";
open(my $inFile, '<:encoding(UTF-8)', $fileName)
    or die "Could not open file '$fileName' $!";
open(my $outFile, '>:encoding(UTF-8)', $outFileName)
    or die "Could not open file '$outFileName' $!";
process02to04($fileName);
while (my $row = <$inFile>) {
    chomp $row;
    # Remove the HTML entities
    $row =~ s/&#x([a-zA-Z0-9]{1,4});?/padHex $1/eg; # hexadecimal number
    $row =~ s/&#([0-9]{1,4});?/decToHex $1/eg; # decimal number
    $row =~ s/&([a-zA-Z0-9]+);?/entToHex $1/eg; # HTML entity
    print $outFile "$row\n";
}
close $inFile or die "Could not close file '$fileName' $!";
close $outFile or die "Could not close file '$outFileName' $!";
`rm $fileName`;
`mv $outFileName $fileName`;
