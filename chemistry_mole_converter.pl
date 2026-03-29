#!/usr/bin/perl
use strict;
use warnings;

# chemistry_mole_converter.pl
# Converts grams to moles for a few classroom substances.

my %molar_masses = (
    "H2O"  => 18.015,
    "CO2"  => 44.01,
    "O2"   => 32.00,
    "NaCl" => 58.44,
    "C6H12O6" => 180.16,
);

print "Chemistry Mole Converter\n";
print "Available substances: H2O, CO2, O2, NaCl, C6H12O6\n";
print "Enter formula: ";
chomp(my $formula = <STDIN>);

if (!exists $molar_masses{$formula}) {
    print "Unknown formula.\n";
    exit;
}

print "Enter mass in grams: ";
chomp(my $grams = <STDIN>);

if ($grams !~ /^\d*\.?\d+$/) {
    print "Mass must be numeric.\n";
    exit;
}

my $moles = $grams / $molar_masses{$formula};
print "\nFormula: $formula\n";
print "Molar mass: $molar_masses{$formula} g/mol\n";
print "Moles = mass / molar mass\n";
print "Moles = $grams / $molar_masses{$formula} = $moles mol\n";
