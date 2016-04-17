import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ie.crf.*;
import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.sequences.DocumentReaderAndWriter;
import edu.stanford.nlp.util.Triple;

import edu.stanford.nlp.tagger.maxent.MaxentTagger;

import java.util.List;


import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main 	
{
	

public static < T > void printArray(T[] t){
	for (T e:t){
    System.out.println(e);
	}
}
		
  public static void main(String[] args) throws Exception {
	   AbstractSequenceClassifier classifier;
	   classifier = CRFClassifier.getClassifierNoExceptions("/Users/cenkbahcevan/Desktop/ExtractDLPR/stanford-ner-2015-12-09/classifiers"
	   		+ "/english.all.3class.distsim.crf.ser.gz");
	  
	   String[] example = {"Gozde Sinturk was born on 12 April",
       "I go to school at Stanford University, which is located in California." };
 for (String str : example) {
System.out.println(classifier.classifyToString(str));
System.out.println();
}

	   
	  
	   
	  
    
  }
}
