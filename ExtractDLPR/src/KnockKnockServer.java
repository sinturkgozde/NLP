import java.net.*;
import java.io.*;

import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ie.crf.CRFClassifier;
 
public class KnockKnockServer {
    public static void main(String[] args) throws IOException {
	   AbstractSequenceClassifier classifier;
	   classifier = CRFClassifier.getClassifierNoExceptions("classifiers"
			   + "/english.all.3class.distsim.crf.ser.gz");
	   String classifierPath = "classifiers/english.all.3class.distsim.crf.ser.gz";
	   Extractor x = new Extractor(classifierPath);
//        if (args.length != 1) {
//            System.err.println("Usage: java KnockKnockServer <port number>");
//            System.exit(1);
//        }
		String pn = "3000";
    	int portNumber = Integer.parseInt(pn);
    	//String classifierPath = ""
 
        try ( 
            ServerSocket serverSocket = new ServerSocket(portNumber);
            Socket clientSocket = serverSocket.accept();
            PrintWriter out =
                new PrintWriter(clientSocket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream()));
        ) {
         
            String inputLine, outputLine;
             
            // Initiate conversation with client
            KnockKnockProtocol kkp = new KnockKnockProtocol();
            outputLine = kkp.processInput(null);
            System.out.println(outputLine);
            System.out.println("Burda 1");
            while ((inputLine = in.readLine()) != null) {
                outputLine = kkp.processInput(inputLine);
                String[] data = inputLine.split(" ");
                for(String sen : data){
                	 classifier.classifyToString(sen);
                	 out.println(classifier.classifyToString(sen));
                }
                
                out.println(outputLine);
                System.out.println("Burda 2");
                
              
                if (inputLine.equals("Bye."))
                    break;
            }
        } catch (IOException e) {
            System.out.println("Exception caught when trying to listen on port "
                + portNumber + " or listening for a connection");
            System.out.println(e.getMessage());
        }
        
    }
}