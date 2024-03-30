cdef extern from "SCF_PEKS.h":
    ctypedef struct COMMONPARAMETER:
        pass
    ctypedef struct PUBLICKEYSERVER:
        pass
    ctypedef struct SECRET:
        pass
    ctypedef struct mpz_t:
        pass
    ctypedef struct element_t:
        pass

    void SCF_Setup(COMMONPARAMETER* cp, size_t k)
    void SCF_KeyGenServer(COMMONPARAMETER cp, mpz_t skS, PUBLICKEYSERVER* pkS)
    void SCF_KeyGenReceiver(COMMONPARAMETER cp, mpz_t skR, element_t pkR)
    void SCF_PEKS(COMMONPARAMETER cp, PUBLICKEYSERVER pkS, element_t pkR, char* keyword, SECRET* S)
    void SCF_Trapdoor(COMMONPARAMETER cp, mpz_t skR, char* keyword, element_t Tw)
    int SCF_Test(COMMONPARAMETER cp, SECRET S, element_t Tw, mpz_t skS, PUBLICKEYSERVER pkS, char* keyword)
    void SCF_deleteCommonParameter(COMMONPARAMETER* cp)


cdef COMMONPARAMETER cp
cdef size_t k=256
cdef PUBLICKEYSERVER pkS
cdef element_t pkR
cdef mpz_t skS, skR
cdef SECRET S
cdef element_t Tw

def setup():
    SCF_Setup(&cp, k)
    SCF_KeyGenServer(cp, skS, &pkS)
    SCF_KeyGenReceiver(cp, skR, pkR)

def certificate(keyword_string):
    cdef bytes keyword_bytes = keyword_string.encode('utf-8')
    cdef char* keyword = keyword_bytes
    SCF_PEKS(cp, pkS, pkR, keyword, &S)

def getSearchMail(keyword_string):
    cdef bytes keyword_bytes = keyword_string.encode('utf-8')
    cdef char* keyword = keyword_bytes

    SCF_Trapdoor(cp, skR, keyword, Tw);
    cdef int result = SCF_Test(cp, S, Tw, skS, pkS, keyword)
    if result == 1:
        print("SCF Test passed: Keyword is matched.\n")
        return 1
    else:
        print("SCF Test failed: Keyword is not matched.\n")
        return 0

def example():
    return "SCF"