import pytest
from distributerbot.service.auth_manager import AuthorityManager

auth_manager = AuthorityManager('TEST_AUTH.txt')

def test_add_auth():
    ## setup
    auth_manager.clear_auth()
    
    ## act
    add_new_auth_result = auth_manager.give_auth(1)
    add_existing_auth_result = auth_manager.give_auth(1)

    ## assertion
    assert(add_new_auth_result == True)
    assert(add_existing_auth_result == False)

auth_manager.clear_auth()

def test_remove_auth():
    ## setup
    auth_manager.clear_auth()
    auth_manager.give_auth(2)
    
    ## act
    remove_existing_auth_result = auth_manager.remove_auth(2)
    remove_nonexistent_auth_result = auth_manager.remove_auth(3)

    ## assertion
    assert(remove_existing_auth_result == True)
    assert(remove_nonexistent_auth_result == False)


    
## cleanup
auth_manager.remove_auth_file()