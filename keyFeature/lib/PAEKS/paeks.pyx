cdef extern from "PAEKS.h":
    ctypedef struct PARAM:
        pass
    ctypedef struct mpz_t:
        pass
    ctypedef struct element_t:
        pass

    void PAEKS_Setup(PARAM* param)
    void PAEKS_KeyGenS(PARAM param, element_t PkS, mpz_t SkS)
    void PAEKS_KeyGenR(PARAM param, element_t PkR, mpz_t SkR)
    void PAEKS_PEKS(PARAM param, element_t PkR, mpz_t SkS, char* keyword, element_t C1, element_t C2)
    void PAEKS_Trapdoor(PARAM param, element_t PkS, mpz_t SkR, char* keyword, element_t Tw)
    int PAEKS_Test(PARAM param, element_t C1, element_t C2, element_t Tw, element_t PkS, element_t PkR)
    void PAEKS_deletePARAM(PARAM* param)


cdef PARAM param
cdef element_t PkS, PkR, C1, C2, Tw
cdef mpz_t SkS, SkR

def setup():
    PAEKS_Setup(&param)
    PAEKS_KeyGenS(param, PkS, SkS)
    PAEKS_KeyGenR(param, PkR, SkR)

def certificate(keyword_string):
    cdef bytes keyword_bytes = keyword_string.encode('utf-8')
    cdef char* keyword = keyword_bytes
    PAEKS_PEKS(param, PkR, SkS, keyword, C1, C2)

def getSearchMail(keyword_string):
    cdef bytes keyword_bytes = keyword_string.encode('utf-8')
    cdef char* keyword = keyword_bytes

    PAEKS_Trapdoor(param, PkS, SkR, keyword, Tw)
    cdef int result = PAEKS_Test(param, C1, C2, Tw, PkS, PkR)
    if result == 1 :
        print("PAEKS Test passed: Keyword is matched.\n")
        return 1
    else:
        print("PAEKS Test failed: Keyword is not matched.\n")
        return 0

def example():
    return "PAEKS"