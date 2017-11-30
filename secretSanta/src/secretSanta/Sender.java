package secretSanta;

import java.util.Properties;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

import java.util.Calendar;
import java.util.Date;

public class Sender {
	
	private Session session;
	
	private final String username = "dkolano2@gmail.com";
	private final String password = "dBeasT11";
	private final String host = "smtp.gmail.com";
	private final String sender = "Santa@gmail.com";
	
	Sender(){
		Properties properties = System.getProperties();
		//properties.put("mail.smtp.ssl.enable", "true");
		properties.put("mail.smtp.auth", "true");
		properties.put("mail.smtp.starttls.enable", "true");
		properties.put("mail.smtp.host", host);
		properties.put("mail.smtp.port", "587");
		properties.put("mail.smtp.from", "Santa");

		session = Session.getInstance(properties,new javax.mail.Authenticator() {
			protected PasswordAuthentication getPasswordAuthentication() {
				return new PasswordAuthentication(username,password);
			}
		});
	}
	
	void sendMessage(String address,String subj,String body) {
		
		try {
			MimeMessage message = new MimeMessage(session);
			message.setFrom(new InternetAddress(username));
			message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(address));
			message.setSubject(subj);
			message.setSender(new InternetAddress(sender));
			Calendar cal = Calendar.getInstance();
			cal.set(2017, 11, 25);
			message.setSentDate(cal.getTime());
			message.setContent(body,"text/html");
			Transport.send(message);
		} catch (MessagingException mex) {
			mex.printStackTrace();
		}
	}
}
