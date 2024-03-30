from libc.stdlib cimport malloc
cdef extern from "string.h":
    char* strcpy(char* dest, char* src)
    char *strncpy(char *string1, const char *string2, size_t count);

cdef extern from "PKE_PEKS.h":
    ctypedef struct PARAMETER:
        pass
    ctypedef struct mpz_t:
        pass
    ctypedef struct element_t:
        pass

    void PKE_Setup(PARAMETER* params)
    void PKE_KeyGen(PARAMETER params, mpz_t sk, element_t pk)
    void PKE_Encrypt(PARAMETER params, element_t pk, char* w, char* plaintext, element_t c1, char** c2, char** tau, char** sigma)
    void PKE_Trapdoor(PARAMETER params, mpz_t sk, char* w, element_t tw)
    int PKE_Test(PARAMETER params, element_t c1, char* tau, element_t tw)
    char* PKE_Decrypt(PARAMETER params, mpz_t sk, element_t c1, char* c2, char* tau, char* sigma)
    void PKE_deletePARAMETER(PARAMETER* params)


cdef PARAMETER params
cdef element_t pk
cdef mpz_t sk
cdef element_t c1, tw
cdef char* c2 = NULL
cdef char* tau = NULL
cdef char* sigma = NULL

def setup():
    PKE_Setup(&params)
    PKE_KeyGen(params, sk, pk)

def getCyphertext(keyword_string, plaintext_string):
    cdef bytes keyword_bytes = keyword_string.encode('utf-8')
    cdef char* keyword = keyword_bytes
    cdef bytes plaintext_bytes = plaintext_string.encode('utf-8')
    cdef char* plaintext = plaintext_bytes

    PKE_Encrypt(params, pk, keyword, plaintext, c1, &c2, &tau, &sigma)
    cdef char buffer[256]  # Adjust the buffer size as needed
    strcpy(buffer, sigma)
    print(buffer, "\n")
    return buffer.decode("utf-8", errors="replace")

def getSearchMail(keyword_string):
    cdef bytes keyword_bytes = keyword_string.encode('utf-8')
    cdef char* keyword = keyword_bytes

    PKE_Trapdoor(params, sk, keyword, tw)
    cdef int test_result = PKE_Test(params, c1, tau, tw)
    if test_result == 1:
        print("PKE Test passed: Keyword is matched.\n")
        return 1
    else :
        print("PKE Test failed: Keyword is not matched.\n")
        return 0

def pke_dec(sigma_string):
    cdef char* sigma_encode 
    sigma_encode = <char*>malloc((len(sigma_string) + 1) * sizeof(char))
    strncpy(sigma_encode, sigma_string.encode('utf-8'), len(sigma_string))
    sigma_encode[len(sigma_string)] = '\0'
    print(sigma_encode, "\n")

    cdef char* message = PKE_Decrypt(params, sk, c1, c2, tau, sigma)
    print("PKE Decrypted Message:\n", message, "\n")
    cdef char buffer[256]
    strcpy(buffer, message)
    return buffer.decode("utf-8", errors="replace")

def example():
    return "PKE"