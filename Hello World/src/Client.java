
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.Line.Info;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.Mixer;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.TargetDataLine;

public class Client {
boolean stopCapture = false;
AudioFormat audioFormat;
TargetDataLine targetDataLine;
public static void main(String[] args) throws LineUnavailableException {
	Mixer mixer = AudioSystem.getMixer(null); // default mixer
	mixer.open();

	System.out.printf("Supported SourceDataLines of default mixer (%s):\n\n", mixer.getMixerInfo().getName());
	for(Info info : mixer.getSourceLineInfo()) {
	    if(SourceDataLine.class.isAssignableFrom(info.getLineClass())) {
	        SourceDataLine.Info info2 = (SourceDataLine.Info) info;
	        System.out.println(info2);
	        System.out.printf("  max buffer size: \t%d\n", info2.getMaxBufferSize());
	        System.out.printf("  min buffer size: \t%d\n", info2.getMinBufferSize());
	        AudioFormat[] formats = info2.getFormats();
	        System.out.println("  Supported Audio formats: ");
	        for(AudioFormat format : formats) {
	            System.out.println("    "+format);
//	          System.out.printf("      encoding:           %s\n", format.getEncoding());
//	          System.out.printf("      channels:           %d\n", format.getChannels());
//	          System.out.printf(format.getFrameRate()==-1?"":"      frame rate [1/s]:   %s\n", format.getFrameRate());
//	          System.out.printf("      frame size [bytes]: %d\n", format.getFrameSize());
//	          System.out.printf(format.getSampleRate()==-1?"":"      sample rate [1/s]:  %s\n", format.getSampleRate());
//	          System.out.printf("      sample size [bit]:  %d\n", format.getSampleSizeInBits());
//	          System.out.printf("      big endian:         %b\n", format.isBigEndian());
//	          
//	          Map<String,Object> prop = format.properties();
//	          if(!prop.isEmpty()) {
//	              System.out.println("      Properties: ");
//	              for(Map.Entry<String, Object> entry : prop.entrySet()) {
//	                  System.out.printf("      %s: \t%s\n", entry.getKey(), entry.getValue());
//	              }
//	          }
	        }
	        System.out.println();
	    } else {
	        System.out.println(info.toString());
	    }
	    System.out.println();
	}

	mixer.close();
    Client tx = new Client();
    tx.captureAudio();
	//listMixers();
}
private void captureAudio() {
    try {
        Mixer.Info[] mixerInfo = AudioSystem.getMixerInfo();
        audioFormat = getAudioFormat();
        DataLine.Info dataLineInfo = new DataLine.Info(
                TargetDataLine.class, audioFormat);
        Mixer mixer = AudioSystem.getMixer(mixerInfo[2]);

        targetDataLine = (TargetDataLine) mixer.getLine(dataLineInfo);
        targetDataLine.open(audioFormat);
        targetDataLine.start();

        Thread captureThread = new CaptureThread();
        captureThread.start();

    } catch (Exception e) {
        System.out.println(e);
        System.exit(0);
    }
}
class CaptureThread extends Thread {

    byte tempBuffer[] = new byte[10000];

    @Override
    public void run() {
        stopCapture = false;
        try {
            while (!stopCapture) {
                int cnt = targetDataLine.read(tempBuffer, 0,
                        tempBuffer.length);
                System.out.println(tempBuffer);
           }
           } catch (Exception e) {
            System.out.println(e);
            System.exit(0);
        }
    }
}

public static void listMixers(){
    System.out.println("Available mixers:");
    Mixer.Info[] mixerInfo = AudioSystem.getMixerInfo();
    //System.out.println(mixerInfo[0]);
    for(int arrayIndex = 0; arrayIndex < mixerInfo.length;  arrayIndex++){
		//mixerDatas[arrayIndex] = mixerInfo[arrayIndex].getName();
          
          System.out.println("Mixer: "+mixerInfo[arrayIndex]);
       
    }
  }

private AudioFormat getAudioFormat() {
    float sampleRate = 80000.0F;

    int sampleSizeInBits = 16;

    int channels = 2;

    boolean signed = true;

    boolean bigEndian = false;

    return new AudioFormat(sampleRate, sampleSizeInBits, channels, signed,
            bigEndian);
}}