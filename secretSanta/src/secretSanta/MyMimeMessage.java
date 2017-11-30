package secretSanta;

import java.io.InputStream;

import javax.mail.Folder;
import javax.mail.MessagingException;
import javax.mail.Session;
import javax.mail.internet.InternetHeaders;
import javax.mail.internet.MimeMessage;

public class MyMimeMessage extends MimeMessage {

	public MyMimeMessage(Session session) {
		super(session);
		// TODO Auto-generated constructor stub
	}

	public MyMimeMessage(MimeMessage arg0) throws MessagingException {
		super(arg0);
		// TODO Auto-generated constructor stub
	}

	public MyMimeMessage(Session session, InputStream is) throws MessagingException {
		super(session, is);
		// TODO Auto-generated constructor stub
	}

	public MyMimeMessage(Folder folder, int msgnum) {
		super(folder, msgnum);
		// TODO Auto-generated constructor stub
	}

	public MyMimeMessage(Folder folder, InputStream is, int msgnum) throws MessagingException {
		super(folder, is, msgnum);
		// TODO Auto-generated constructor stub
	}

	public MyMimeMessage(Folder folder, InternetHeaders headers, byte[] content, int msgnum) throws MessagingException {
		super(folder, headers, content, msgnum);
		// TODO Auto-generated constructor stub
	}
	
	@Override
	protected void updateMessageID() throws MessagingException {
		setHeader("Message-ID", "<" + "Santa" + "@" + "NorthPole.com" + ">");
	}

}
