<center> <h1>XSS Test Report</h1> </center>

## No Authentication

|      | Route/URL                      | Parameter | XSS successful? |
|:----:|--------------------------------|:---------:|:--------------------------:|
| Scan  | http://127.0.0.1:8081/         |  login  |             NO             |
| Scan  | http://127.0.0.1:8081/user/login    | email  |             NO           |
| Scan  | http://127.0.0.1:8081/user/login    | password  |             NO           |  
| Scan | http://127.0.0.1:8081/user/register | email |             NO             |
| Scan | http://127.0.0.1:8081/user/register | name |             NO             |
| Scan | http://127.0.0.1:8081/user/register | password |             NO             |


## With Authentication

|      | Route/URL                      | Parameter | XSS successful? |
|:----:|--------------------------------|:---------:|:--------------------------:|
| Scan | http://127.0.0.1:8081/user/logout       | N/A  |    NO             |  
| Scan | http://127.0.0.1:8081/user/modify | username  |             NO             |
| Scan | http://127.0.0.1:8081/user/modify | shipping  |             NO             |
| Scan | http://127.0.0.1:8081/user/modify | postal  |             NO             |
| Scan | http://127.0.0.1:8081/product/create | name |             NO             |  
| Scan | http://127.0.0.1:8081/product/create | description |           NO           |  
| Scan | http://127.0.0.1:8081/product/create | price |             NO             |  





## 1. We did two rounds of scanning. Why the results are different? What is the purpose of adding in the session id?
After the user logged, the browser stores the following cookie with authentication information for the server. This allows the user access to parts of the page that weren't accessible otherwise. The overall results were the same, showing no vulnerabilities reguardless of authentication. However, providing the authentication token to the XSS script injector gave it access to three new sections of the website as well as the users personal information. This is not a cause for concern as all XSS tests passed before providing authentication. Therefore, it would be difficult for a hacker to obtain the authentication token from the cookie. The purpose of adding the session id is to allow for a more thorough test of the entire site instead of only the login and register pages. While authenticated, XSS attacks can be more dangerous because of potential stored XSS. For example, a user logs into the application with a stored unwanted XSS. It is possible that the user clicks on a malicious link that points back to the XSS hole and get exploited.

## 2. Are all the possible XSS (script injection) links/routes covered in the table above? (think about any links that will render user inputs, such as URL paramer, cookies, flask flash calls). If not, are those link/pages vulnerable to XSS?
Although this tool may prove useful for a quick XSS vulnerability scan, it is not thorough nor affective against any level of defence. Simple payloads such as "alert()" will not make it through. Although QBAY passed all of the tests, this does not mean that it is not vulnerable. Higher level XSS with input field filter bypas techniques might reveal possible XSS vulnerabilities. All possible routes and links were covered, but not every input field. The team manually tested the input fields with common XSS attacks that were not covered by PWNXSS. There were no indications of possible vulnerabilities. XSS through Flask flash calls is not possible due to the way we configured the failed input responses. We do not pass the user input to the DOM, we simply supply a standard generic error message to indicate which input field was incorrectly supplied.
</br>
