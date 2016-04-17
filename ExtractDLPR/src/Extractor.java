import java.util.ArrayList;
import java.util.List;

import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ie.crf.CRFClassifier;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.util.CoreMap;

/***
 * 
 * @author cenkbahcevan
 * 
 *
 */

public class Extractor {
	
	AbstractSequenceClassifier<CoreMap> sentenceClassifier;
	
	private ArrayList<String> personList;
	private ArrayList<String> locationList;
	private ArrayList<String> organizationList;
	private AbstractSequenceClassifier classifier;
	
	public Extractor(String classifierPath) {
		  this.classifier = CRFClassifier.getClassifierNoExceptions(classifierPath);
		  this.personList = new ArrayList<String>();
		  this.locationList = new ArrayList<String>();
		  this.organizationList = new ArrayList<String>();
	}
	
	
	public void extractFromSentence(String str){
		String[] splittedSentence = str.split(" ");
		for (int i=0;i<splittedSentence.length;i++){
			splittedSentence[i] =this.classifier.classifyToString(splittedSentence[i]);
		}
		for (String element:splittedSentence){
			String[] splittedPart = element.split("/");
			if (splittedPart[1].equals("PERSON")){
				this.personList.add(splittedPart[0]);
				
			}
			else if (splittedPart[1].equals("LOCATION")){
				this.locationList.add(splittedPart[0]);
			}
			else if (splittedPart[1].equals("ORGANIZATION")){
					this.organizationList.add(splittedPart[0]);
		}
	}
		
		System.out.println();
	
	
	
	}
	@Override
	public String toString() {
		String str = "Persons:";
		for (String s:this.personList){
			str  = str+" "+s;
		}
		str += "\n\nLocations";
		for (String s:this.locationList){
			str  = str+" "+s;
		}
		str += "\n\nOrganizations";
		for (String s:this.organizationList){
			str  = str+" "+s;
		}
		return str;
	}
	

}
