import java.io.*;
import java.util.ArrayList;
import java.util.Random;
import java.net.Socket;
import java.util.StringTokenizer;

public class HTTPdriver extends Thread 
{
	String tag, server, urlfile;
	int hits, port;
	
	public HTTPdriver(String t, String s, String uf, int h) {
		tag = t;
		server = s;
		urlfile = uf;
		hits = h;
	}

	public void run() {
		try {
		
		Random randomGenerator = new Random();
		String line;
		Socket soc;
		int i, n;
		long starttime;
	
		//System.out.println("* ["+tag+"] ["+server+"] ["+hits+"] ["+urlfile+"]");
		
		FileReader instream = new FileReader(new File(urlfile));
        BufferedReader in = new BufferedReader(instream);
		StringTokenizer t = new StringTokenizer(server, ":");
		if(t.countTokens() > 1) {
			server = t.nextToken(); 
			port = Integer.parseInt(t.nextToken());
		} else 
			port = 80;
		
		ArrayList urls = new ArrayList();	
		while((line = in.readLine()) !=  null)
			if (randomGenerator.nextInt(100)>50) {
				urls.add(line);
				//System.out.println("--> Añadida URL: " + line + "\n");
			}
			else{
				//System.out.println("*****> Descartada: " + line + "\n");
			}
		in.close();

		for(n=0;n<hits;n++) {
			soc = new Socket(server, port);
			BufferedWriter wr = new BufferedWriter
					(new OutputStreamWriter(soc.getOutputStream(),"UTF8"));
			BufferedReader socin = new BufferedReader
					(new InputStreamReader(soc.getInputStream()));
			starttime = System.currentTimeMillis();

			for(i=0;i<urls.size();i++) {


				URLhandler url = new URLhandler
							((String) urls.get(i));
				wr.write(url.getRequest());
				wr.flush();
				//report(socin.readLine(), (String) urls.get(i), starttime);
			}
			//soc.shutdownInput();
			
			soc.shutdownOutput();
			soc.close();
			System.out.print("--> ["+server+":"+port+"]: "+ Integer.toString(urls.size()) + " urls");
			System.out.println(". Response in "+(System.currentTimeMillis()-starttime)+" ms");
			
		}
		
		} catch(Exception e) {
			System.out.println("ERROR: Error accessing "+urlfile);
			System.exit(1);
		}
	}

	public synchronized void report(String msg, String url, long starttime) {
		System.out.println("["+server+":"+port+"]"+url);
		System.out.print("Response :"+msg);
		System.out.println(" ("+(System.currentTimeMillis()-starttime)+" ms)");
	}
}
