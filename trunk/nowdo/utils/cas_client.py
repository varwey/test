# -*- coding=utf-8 -*-
import urllib

# Status codes returned internally by function get_ticket_status().
TICKET_NONE = -1  # Invalid CAS server ticket found.
TICKET_INVALID = 0  # Invalid CAS server ticket found.
TICKET_OK = 1  # Valid CAS server ticket found.


def login_url(cas_host, service_url):
    cas_url = cas_host + "/login?service=" + service_url
    return cas_url


def logout_url(cas_host, redirect_url):
    cas_url = cas_host + "/logout?service=" + redirect_url
    return cas_url


def get_ticket_status(cas_host, service_url, ticket):
    if ticket:
        cas_validate = cas_host + "/serviceValidate?ticket=" + ticket + "&service=" + service_url
        f_validate = urllib.urlopen(cas_validate)
        #  Get first line - should be yes or no
        response = f_validate.read()
        #        print response
        user_id = parse_tag(response, "cas:user")
        #  Ticket does not validate, return error
        if user_id == "":
            return TICKET_INVALID, ""
        #  Ticket validates
        else:
            return TICKET_OK, user_id
    return TICKET_NONE, ""


def get_logout_request_ticket(logout_request):
    return parse_tag(logout_request, "samlp:SessionIndex")


def parse_tag(string, tag):
    """
    #  Used for parsing xml.  Search str for first occurrence of
    #  <tag>.....</tag> and return text (striped of leading and
    #  trailing whitespace) between tags.  Return "" if tag not
    #  found.
    """
    tag1_pos1 = string.find("<" + tag)
    #  No tag found, return empty string.
    if tag1_pos1 == -1:
        return ""
    tag1_pos2 = string.find(">", tag1_pos1)
    if tag1_pos2 == -1:
        return ""
    tag2_pos1 = string.find("</" + tag, tag1_pos2)
    if tag2_pos1 == -1:
        return ""
    return string[tag1_pos2 + 1:tag2_pos1].strip()