import java.io.*;
import java.util.*;

class traffic {

	public static void main(String args[]) throws IOException {
		String line;
		int i;

		//FileReader instream= new FileReader(new File("servers.txt"));
		FileReader instream= new FileReader(new File(args[0]));
		BufferedReader in = new BufferedReader(instream);
		
		Vector tpool = new Vector();

		//System.out.println("HTTP Traffic Generator | Vikram Rangnekar <vr@udel.edu>");
		while((line = in.readLine()) !=  null) {
			StringTokenizer tok;
			
			if(line.startsWith("#")) 
				continue;	

			tok = new StringTokenizer(line);
			tpool.add(new HTTPdriver(tok.nextToken(),
						tok.nextToken(),
						tok.nextToken(),
						Integer.parseInt(tok.nextToken())));
		
		}
		in.close();
		
		for(i=0;i<tpool.size();i++) {
			HTTPdriver driver = (HTTPdriver) tpool.elementAt(i);
			//driver.setDaemon(true);
			driver.start();		
		}
	}

}
