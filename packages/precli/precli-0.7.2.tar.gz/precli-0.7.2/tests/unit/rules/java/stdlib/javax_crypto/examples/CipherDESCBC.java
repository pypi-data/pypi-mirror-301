// level: ERROR
// start_line: 14
// end_line: 14
// start_column: 40
// end_column: 62
import java.security.*;
import javax.crypto.*;


public class CipherDESCBC {
    public static void main(String [] args) {
        Cipher cipher = null;
        try {
            cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
        } catch (NoSuchAlgorithmException exception) {
            exception.printStackTrace();
        } catch (NoSuchPaddingException exception) {
            exception.printStackTrace();
        }
    }
}
