import io
import re
from more_termcolor import colored, cprint
from more_termcolor.tests.common import print_and_compare, codes_perm


###########################
## Different reset codes ##
###########################

# Trivial
#########


@print_and_compare
class Test_1_inside_color:
    
    def test__red_dark_red(self):
        """R    F       /F/B
           31   2   →   22"""
        dark = colored(' Dark ', 'dark')
        assert dark == '\x1b[2m Dark \x1b[22m'
        red_dark_red = colored(' Red ' + dark + ' Red ', 'red') + ' NORMAL'
        expected = '\x1b[31m Red \x1b[2m Dark \x1b[22m Red \x1b[39m NORMAL'
        
        # smart reset dark in the middle, and does not re-open red
        return red_dark_red, expected
    
    def test__italic_bold_italic(self):
        """I    B       /F/B
           3    1   →   22"""
        bold = colored(' Bold ', 'bold')
        italic_bold_italic = colored(' Italic ' + bold + ' Italic ', 'italic') + ' NORMAL'
        expected = '\x1b[3m Italic \x1b[1m Bold \x1b[22m Italic \x1b[23m NORMAL'
        
        return italic_bold_italic, expected
    
    def test__bold_red_bold(self):
        """I    R       /FG
           3    31  →   39"""
        red = colored(' Red ', 'red')
        assert red == '\x1b[31m Red \x1b[39m'
        bold_red_bold = colored(' Bold ' + red + ' Bold ', 'bold') + ' NORMAL'
        expected = '\x1b[1m Bold \x1b[31m Red \x1b[39m Bold \x1b[22m NORMAL'
        
        return bold_red_bold, expected
    
    def test__italic_brightgreen_italic(self):
        """I    SG      /FG
           3    92  →   39"""
        brightgreen = colored(' BrightGreen ', 'bright green')
        assert brightgreen == '\x1b[92m BrightGreen \x1b[39m'
        italic_brightgreen_italic = colored(' Italic ' + brightgreen + ' Italic ', 'italic') + ' NORMAL'
        expected = '\x1b[3m Italic \x1b[92m BrightGreen \x1b[39m Italic \x1b[23m NORMAL'
        
        return italic_brightgreen_italic, expected
    
    def test__bold_italic_bold(self):
        """B    I       /I
           1    3   →   23"""
        italic = colored(' Italic ', 'italic')
        assert italic == '\x1b[3m Italic \x1b[23m'
        bold_italic_bold = colored(' Bold ' + italic + ' Bold ', 'bold') + ' NORMAL'
        expected = '\x1b[1m Bold \x1b[3m Italic \x1b[23m Bold \x1b[22m NORMAL'
        
        # smart reset italic (23), no reopen bold
        return bold_italic_bold, expected
    
    def test__brightwhite_dark_brightwhite(self):
        """S    F       /F
           97   2   →   22"""
        dark = colored(' Dark ', 'dark')
        assert dark == '\x1b[2m Dark \x1b[22m'
        brightwhite_dark_brightwhite = colored(' Bright ' + dark + ' Bright ', 'bright white') + ' NORMAL'
        expected = '\x1b[97m Bright \x1b[2m Dark \x1b[22m Bright \x1b[39m NORMAL'
        # smart reset dark, no re-open bright
        
        return brightwhite_dark_brightwhite, expected
    
    def test__brightwhite_red_brightwhite(self):
        """S    R       S
           97   31  →   97"""
        red = colored(' Red ', 'red')
        assert red == '\x1b[31m Red \x1b[39m'
        brightwhite_red_brightwhite = colored(' Bright ' + red + ' Bright ', 'bright white') + ' NORMAL'
        expected = '\x1b[97m Bright \x1b[31m Red \x1b[97m Bright \x1b[39m NORMAL'
        
        return brightwhite_red_brightwhite, expected
    
    def test__red_onblack_red(self):
        onblack = colored(' OnBlack ', 'on black')
        red_onblack_red = colored(' Red ' + onblack + ' Red ', 'red') + ' NORMAL'
        expected = '\x1b[31m Red \x1b[40m OnBlack \x1b[49m Red \x1b[39m NORMAL'
        
        return red_onblack_red, expected
    
    def test__brightred_onblack_brightred(self):
        onblack = colored(' OnBlack ', 'on black')
        assert onblack == '\x1b[40m OnBlack \x1b[49m'
        brightred_onblack_brightred = colored(' BrightRed ' + onblack + ' BrightRed ', 'bright red') + ' NORMAL'
        expected = "\x1b[91m BrightRed \x1b[40m OnBlack \x1b[49m BrightRed \x1b[39m NORMAL"
        
        return brightred_onblack_brightred, expected
    
    def test__onblack_brightred_onblack(self):
        brightred = colored(' BrightRed ', 'bright red')
        onblack_brightred_onblack = colored(' OnBlack ' + brightred + ' OnBlack ', 'on black') + ' NORMAL'
        expected = '\x1b[40m OnBlack \x1b[91m BrightRed \x1b[39m OnBlack \x1b[49m NORMAL'
        
        return onblack_brightred_onblack, expected
    
    def test__onblack_underline_onblack(self):
        underline = colored(' Underline ', 'ul')
        onblack_underline_onblack = colored(' OnBlack ' + underline + ' OnBlack ', 'on black') + ' NORMAL'
        expected = '\x1b[40m OnBlack \x1b[4m Underline \x1b[24m OnBlack \x1b[49m NORMAL'
        
        return onblack_underline_onblack, expected
    
    def test__underline_onblack_underline(self):
        onblack = colored(' OnBlack ', 'on black')
        underline_onblack_underline = colored(' Underline ' + onblack + ' Underline ', 'underline') + ' NORMAL'
        expected = '\x1b[4m Underline \x1b[40m OnBlack \x1b[49m Underline \x1b[24m NORMAL'
        
        return underline_onblack_underline, expected


@print_and_compare
class Test_2_inside_colors:
    
    def test__brightred__onblack_bold__brightred(self):
        onblackbold = colored(' OnBlackBold ', 'on black', 'bold')
        assert onblackbold == '\x1b[40;1m OnBlackBold \x1b[49;22m'
        brightred_onblackbold_brightred = colored(' BrightRed ' + onblackbold + ' BrightRed ', 'bright red') + ' NORMAL'
        
        expected = f"\x1b[91m BrightRed \x1b[40;1m OnBlackBold \x1b[49;22m BrightRed \x1b[39m NORMAL"
        
        return brightred_onblackbold_brightred, expected
    
    def test__onblack__brightred_bold__onblack(self):
        brightredbold = colored(' BrightRedBold ', 'bright red', 'bold')
        assert brightredbold == '\x1b[91;1m BrightRedBold \x1b[39;22m'
        onblack_brightredbold_onblack = colored(' OnBlack ' + brightredbold + ' OnBlack ', 'on black') + ' NORMAL'
        expected = f'\x1b[40m OnBlack \x1b[91;1m BrightRedBold \x1b[39;22m OnBlack \x1b[49m NORMAL'
        
        return onblack_brightredbold_onblack, expected
    
    def test__bold__green_on_black__bold(self):
        greenonblack = colored(' GreenOnBlack ', 'green', 'on black')
        bold_greenonblack_bold = colored(' Bold ' + greenonblack + ' Bold ', 'bold') + ' NORMAL'
        expected = f'\x1b[1m Bold \x1b[32;40m GreenOnBlack \x1b[39;49m Bold \x1b[22m NORMAL'
        return bold_greenonblack_bold, expected


@print_and_compare
class Test_2_outside_colors:
    
    def test__redonblack__bold__redonblack(self):
        bold = colored(' Bold ', 'bold')
        redonblack__bold__redonblack = colored(' RedOnBlack ' + bold + ' RedOnBlack ', 'red', 'on black') + ' NORMAL'
        expected = f'\x1b[31;40m RedOnBlack \x1b[1m Bold \x1b[22m RedOnBlack \x1b[39;49m NORMAL'
        
        return redonblack__bold__redonblack, expected
    
    def test__underlineonblack__red__underlineonblack(self):
        red = colored(' Red ', 'red')
        underlineonblack__red__underlineonblack = colored(' UnderlineOnBlack ' + red + ' UnderlineOnBlack ', 'ul', 'on black') + ' NORMAL'
        expected = f'\x1b[4;40m UnderlineOnBlack \x1b[31m Red \x1b[39m UnderlineOnBlack \x1b[24;49m NORMAL'
        
        return underlineonblack__red__underlineonblack, expected
    
    def test__underlinegreen__onblack__underlinegreen(self):
        onblack = colored(' OnBlack ', 'on black')
        underlinegreen__onblack__underlinegreen = colored(' UnderlineGreen ' + onblack + ' UnderlineGreen ', 'ul', 'green') + ' NORMAL'
        expected = f'\x1b[4;32m UnderlineGreen \x1b[40m OnBlack \x1b[49m UnderlineGreen \x1b[24;39m NORMAL'
        
        return underlinegreen__onblack__underlinegreen, expected
