# -*- coding: utf-8 -*-
"""
DrupalLibrary.drupalkeywords


Robotframework keywords specific to Drupal control
"""

from urlparse import urljoin

from lxml import etree

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from . import logger

#import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

class KeywordError(RuntimeError):
    pass


class KeywordFatalError(KeywordError):
    ROBOT_EXIT_ON_FAILURE = True


class FailureManager(object):
    """An utility that re-raises the failure exception as "fatal" (stops the RF session)
    if ``exit_on_failure`` param is True
    """
    def __init__(self, exit_on_failure, message=""):
        self.exit_on_failure = exit_on_failure
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            exc_val.ROBOT_EXIT_ON_FAILURE = True


class DrupalKeywords(object):
    """The base class for DrupalLibrary that provides the keywords and utility methods"""

    def __init__(self, home_url):
        """
        `home_url` is the URL of the Drupal site home page.

        Example:
        | ***** Settings ***** |
        | Library | DrupalLibrary | http://localhost/site |
        """
        self.home_url = home_url
        try:
            self.selenium = BuiltIn().get_library_instance('Selenium2Library')
        except RobotNotRunningError:
            # IDE completion and libdoc helper. Do not remove!
            # We should never go there when running RF tests
            import Selenium2Library
            self.selenium = Selenium2Library.Selenium2Library()

    def go_to_home_page(self):
        """As its name says, opens the browser to the Drupal site home page

        This keyword takes no argument

        Example:
        | Go To Home Page |
        """
        self.selenium.go_to(self.home_url)

    def sign_in(self, username, password, exit_on_failure=True):
        """Signing in the site using username and password credentials

        Parameters:
        - `username`: provide a valid user name registered in your site
        - `password`: the associated password
        - `exit_on_failure`: please read the `introduction` about this parameter.

        Examples:
        | *Keyword* | *Param* | *Param* | *Param* | *Comment* |
        | Sign In | johndoe | goodpassword | | # Sign in the site as expected |
        | Sign In | johndoe | badpassword | exit_on_failure=${false} | # Carry on the test suite despite failure |
        """
        sel = self.selenium
        login_url = urljoin(self.home_url, 'user')
        sel.go_to(login_url)
        sel.input_text('id=edit-name', username)
        sel.input_password('id=edit-pass', password)
        sel.click_button('id=edit-submit')

        # Checking...
        with FailureManager(exit_on_failure, "Authentication failed"):
            sel.page_should_contain_link("xpath=//a[contains(@href, '/user/logout')]")

    def add_member(self, username, email, password, active=True, extra_roles=None, exit_on_failure=True):
        """Adding a member to a Drupal site

        Required parameters:
        - `username`: a regular Drupal member new name that copes with the site policy
        - `email`: a valid mail address
        - `password`: the password associated with the `username`

        Optional parameters:
        - `active`: the new user is active by default, otherwise, pass the `active=${flase}` to the keyword
        - `extra_roles`: one or a list of additional roles to grant to this user.
        - `exit_on_failure`: please read the `introduction` about this parameter.

        Examples:
        | Comment | Anonymous can't add users |
        | `Logout` |
        | Add Member | johndoe | johndoe@mydomain.com | # Will fail because anonymous user can't do it |
        | Comment | But an admin can do it |
        | `Sign In` | admin | adminpassword |
        | Add Member | johndoe | johndoe@mydomain.com | # Works as long as there's no registered johndoe user |
        | Comment | Add an additional administrator |
        | Add Member | newadmin | newadmin@mydomain.com | newadminsecret | extra_roles=administrator |
        | Comment | Add and user with several roles |
        | @{addroles}= | administrator | reviewer |
        | Add Member | otherguy | otherguy@mydomain.com | otherguysecret | extra_roles=@{addroles} |

        *Warning*: your actual authentication *must* grant user adding, otherwise the keyword fails.
        """
        sel = self.selenium
        add_member_url = urljoin(self.home_url, 'admin/people/create')
        sel.go_to(add_member_url)

        # Check if we got an "Add user" link
        with FailureManager(exit_on_failure, "You are not allowed to add members"):
            links = sel.get_all_links()
            assert u'toolbar-link-admin-people' in links

        # Let's fill the form
        sel.input_text('id=edit-name', username)
        sel.input_text('id=edit-mail', email)
        sel.input_password('id=edit-pass-pass1', password)
        sel.input_password('id=edit-pass-pass2', password)

        # His/her status
        active_rbv = '1' if bool(active) else '0'
        sel.select_radio_button('status', active_rbv)

        # His/her extra role(s)
        if extra_roles is not None:
            if isinstance(extra_roles, basestring):
                extra_roles = (extra_roles,)

            # Looking for roles labels and widgets
            html = self._actual_html()
            label_elts = html.xpath('//div[@id="edit-roles"]//label')
            input_elts = html.xpath('//div[@id="edit-roles"]//input')
            labels = [l.text.strip().lower() for l in label_elts]

            for extra_role in extra_roles:
                extra_role = extra_role.lower()
                if extra_role in labels:
                    position = labels.index(extra_role)
                    checkbox_id = input_elts[position].attrib['id']
                    checkbox_location = 'id={0}'.format(checkbox_id)
                    sel.select_checkbox(checkbox_location)
                else:
                    logger.warning("Cannot grant unknown role {0} to {1}".format(extra_role, username))

        # Kick it
        sel.submit_form('id=user-register-form')

        # Check potential error
        msg = "Something went wrong when creating user {0}".format(username)
        self._wait_bo_ok_status(exit_on_failure, msg)


    def remove_member(self, username, policy='user_cancel_block', exit_on_failure=True):
        """Removes the member identified by `username`

        Required parameters:
        - `username`: A registered user name

        Optional parameters:
        - `cancel_policy`: What do we do precisely with the user account and his content
        | `cancel_policy=user_cancel_block` | Disable the account and keep its content. *(default)* |
        | `cancel_policy=user_cancel_block_unpublish` |  Disable the account and unpublish its content. |
        | `cancel_policy=user_cancel_reassign` | Delete the account and make its content belong to the Anonymous user. |
        | `cancel_policy=user_cancel_delete |  Delete the account and its content. |

        - `exit_on_failure`: Please read the `introduction` about this parameter

        Examples:
        | Comment | Remove member "foobar" as well as his content |
        | Remove Member | foobar |
        | Comment | Remove member "janedoe" but her content is kept and owned by "anonymous user" |
        | Remove Member | janedoe | policy=user_cancel_delete |

        *Warning*: your actual authentication *must* grant user adding, otherwise the keyword fails.
        """
        sel = self.selenium

        # Going to the people mgmt page
        sel.go_to(urljoin(self.home_url, 'admin/people'))

        # Checking we are granted for this
        with FailureManager(exit_on_failure, "You are not allowed to manage members"):
            links = sel.get_all_links()
            assert u'toolbar-link-admin-people' in links

        # Let's find the usename selection widget
        html = self._actual_html()
        users_table = html.xpath('//table[contains(@class, "sticky-enabled")]')
        with FailureManager(exit_on_failure, "It seems there are no members"):
            assert len(users_table) == 1

        # Let' search for our user index
        users_table = users_table[0]
        users_cbx = users_table.xpath('//tr/td[1]//input/@id')  # checkboxes
        users_tds = users_table.xpath('//tr/td[2]/a/text()')  # names
        for checkbox_id, found_username in zip(users_cbx, users_tds):
            if found_username.lower().strip() == username.lower().strip():
                break
        else:
            # Did not find
            msg = "It seems there is no user named {0}".format(username)
            with FailureManager(exit_on_failure, msg):
                raise KeywordError(msg)

        # Ok, we heve a suitable checkbox_id, we select user and operation
        sel.select_checkbox('id={0}'.format(checkbox_id))
        sel.select_from_list('id=edit-operation', 'cancel')

        # Kick the form
        sel.submit_form('id=user-admin-account')

        # Checking the deletion policy
        with FailureManager(exit_on_failure, "Invalid user removal policy {0}".format(policy)):
            assert policy in (
                'user_cancel_block', 'user_cancel_block_unpublish', 'user_cancel_reassign', 'user_cancel_delete'
            )

        # Okay, let's now play with the deletion option and kick agan the form
        sel.select_radio_button('user_cancel_method', policy)
        sel.submit_form('user-multiple-cancel-confirm')

        # Check potential error
        msg = "Something went wrong when deleting user {0}".format(username)
        self._wait_bo_ok_status(exit_on_failure, msg)

    def logout(self):
        """Anonymizes the user
        """
        sel = self.selenium
        logout_url = urljoin(self.home_url, 'user/logout')
        sel.go_to(logout_url)

    # Privates (scenario)

    def _wait_bo_ok_status(self, exit_on_failure, message="", timeout=5):
        """Assert BO status box is OK after action
        (need to be on a BO page)
        """
        message = "{0}. (Have been waiting for {1} seconds)".format(message, timeout)
        with FailureManager(exit_on_failure, message):
            self.selenium.wait_until_element_is_visible('xpath=//div[@class="messages status"]',
                                                        timeout=timeout, error=message)

    # Privates (technical)

    def _actual_html(self, parsed=True):
        """Returns the actual raw or parsed HTML of the browser
        """
        html_source = self._selenium_browser.get_page_source()
        if parsed:
            return etree.HTML(html_source)
        else:
            return html_source

    @property
    def _selenium_browser(self):
        """The instance of selenium browser actually running to get a fine grained control
        """
        return self.selenium._current_browser()
