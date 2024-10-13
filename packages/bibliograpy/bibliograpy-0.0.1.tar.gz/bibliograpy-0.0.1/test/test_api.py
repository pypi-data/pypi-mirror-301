"""Test module for bibliograpy"""
import sys
import pydoc

from bibliograpy.api import reference, Institution, TechReport, Reference, ReferenceBuilder

IAU = Institution(key="iau", title="International Astronomical Union")

IAU_2006_B1 = TechReport(
    key="iau_2006_b1",
    title="Adoption of the P03 Precession Theory and Definition of the Ecliptic",
    institution=IAU)

def test_dependencies_args_default():
    """test deps command without supplying file"""

    @reference(IAU_2006_B1)
    def toto():
        """ma doc"""

    if sys.version_info.minor == 12:
        assert (pydoc.render_doc(toto) ==
"""Python Library Documentation: function toto in module test_api

t\bto\bot\bto\bo()
    ma doc

    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
""")
    else:
        assert (pydoc.render_doc(toto) ==
"""Python Library Documentation: function toto in module test_api

t\bto\bot\bto\bo()
    ma doc
    
    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
""")

    @reference([IAU_2006_B1, IAU])
    def titi():
        """ma doc avec plusieurs références"""


    if sys.version_info.minor == 12:
        assert (pydoc.render_doc(titi) ==
"""Python Library Documentation: function titi in module test_api

t\bti\bit\bti\bi()
    ma doc avec plusieurs références

    Bibliography:

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(titi) ==
"""Python Library Documentation: function titi in module test_api

t\bti\bit\bti\bi()
    ma doc avec plusieurs références
    
    Bibliography:
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")

    @reference(IAU_2006_B1, IAU)
    def tata():
        """ma doc avec plusieurs références en varargs"""


    if sys.version_info.minor == 12:
        assert (pydoc.render_doc(tata) ==
"""Python Library Documentation: function tata in module test_api

t\bta\bat\bta\ba()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(tata) ==
"""Python Library Documentation: function tata in module test_api

t\bta\bat\bta\ba()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")

def test_custom_reference_builder():

    def custom_wrapper(refs: list[Reference]) -> str:
        if len(refs) == 1:
            return f"\n\nBibliographie: {refs[0].to_pydoc()}\n"
        else:
            result = "\n\nBibliographie:\n\n"
            for r in refs:
                result += f"* {r.to_pydoc()}\n"
            return result

    ref = ReferenceBuilder(reference_wrapper=custom_wrapper)

    @ref(IAU_2006_B1, IAU)
    def tatafr():
        """ma doc avec plusieurs références en varargs"""


    if sys.version_info.minor == 12:
        assert (pydoc.render_doc(tatafr) ==
"""Python Library Documentation: function tatafr in module test_api

t\bta\bat\bta\baf\bfr\br()
    ma doc avec plusieurs références en varargs

    Bibliographie:

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(tatafr) ==
"""Python Library Documentation: function tatafr in module test_api

t\bta\bat\bta\baf\bfr\br()
    ma doc avec plusieurs références en varargs
    
    Bibliographie:
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
