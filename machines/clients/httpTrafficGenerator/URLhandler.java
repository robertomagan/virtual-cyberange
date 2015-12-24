import java.util.StringTokenizer;

public class URLhandler
{
	String request;

	public URLhandler(String line) {
		StringTokenizer tok = new StringTokenizer(line, ",");				
		if(tok.countTokens() > 1) {
			request = tok.nextToken() + " HTTP/1.0\r\n";
			request += "Content-Type: application/x-www-form-urlencoded\r\n";
			request += "\r\n" + tok.nextToken(); 
		}
		else
			request = line + " HTTP/1.0\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n";
	}
	
	public String getRequest() {
		return request;
	}
}
