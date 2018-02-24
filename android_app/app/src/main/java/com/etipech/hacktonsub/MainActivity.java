package com.etipech.hacktonsub;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.Build;
import android.os.Bundle;
import android.os.NetworkOnMainThreadException;
import android.provider.MediaStore;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Long emailLong = System.currentTimeMillis() / 1000;
        String email = emailLong.toString();
        EditText email_input = findViewById(R.id.email_input);
        EditText restaurant_input = findViewById(R.id.restaurant_input);
        email = email + "@HackTonSub.com";
        String restaurant = "53994";
        email_input.setText(email);
        restaurant_input.setText(restaurant);
        final SeekBar mark_input = (SeekBar) findViewById(R.id.mark_input);
        final TextView mark_Value = findViewById(R.id.mark_value);

        mark_input.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                // TODO Auto-generated method stub
                mark_Value.setText(String.valueOf(progress));
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }
        });
    }

    private void toaster(String message, int duration) {
        Context context = getApplicationContext();
        Toast toast = Toast.makeText(context, message, duration);
        toast.show();
    }

    private void postToApi(String email, String restaurant, String mark, Bitmap ticket) {
        System.out.println("J aime les poneys roses");
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        ticket.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream);
        byte[] byteArray = byteArrayOutputStream .toByteArray();
        String encoded = Base64.encodeToString(byteArray, Base64.DEFAULT);
        Intent intent = new Intent(MainActivity.this, DoDoDoThePost.class);
        Bundle b = new Bundle();
        b.putString("email", email);
        b.putString("restaurant", restaurant);
        b.putString("mark", mark);
        b.putString("ticket", encoded);
        intent.putExtras(b);
        System.out.println("J aime beaucoup les poneys roses");
        startActivity(intent);
        System.out.println("J aime tres tres beaucoup les poneys roses");
        /*        System.out.println("POST TO API");
        String url = "https://10.15.192.243:4242";
//        String url = "https://www.google.com";
        try {
            System.out.println("toto tata");
            URL obj = new URL(url);
            System.out.println("ICI");
            HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("User-Agent", "Mozilla/5.0");
            con.setRequestProperty("Accept-Language", "en-US,en; q=0.5");
            Log.e("DEBUG", "email=" + email + "&restaurant= " + restaurant + "&mark=" + mark + "&ticket=" + ticket.toString());
            String urlParameters = "email=" + email + "&restaurant= " + restaurant + "&mark=" + mark + "&ticket=" + ticket.toString();
            con.setDoOutput(true);
            System.out.println("LA");
            DataOutputStream wr = new DataOutputStream(con.getOutputStream());
            System.out.println("LA 0");
            wr.writeBytes(urlParameters);
            System.out.println("LA 1");
            wr.flush();
            wr.close();
            System.out.println("LA 2");
            int responseCode = con.getResponseCode();
            System.out.println("\nSending 'POST' request to URL : " + url);
            System.out.println("Post parameters : " + urlParameters);
            System.out.println("Response Code : " + responseCode);
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuilder response = new StringBuilder();
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            System.out.println(response.toString());
        } catch (IOException e) {
            System.err.println("Error : " + e.getMessage());
            toaster("Server currently unavailable", Toast.LENGTH_SHORT);
        } catch (NetworkOnMainThreadException e){
            System.err.println("JEAN MI");
        }*/
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && null != data) {
            Bundle extras = data.getExtras();
            try {
                extras.get("data");
                Bitmap ticket = (Bitmap) extras.get("data");
                EditText email_input = findViewById(R.id.email_input);
                EditText restaurant_input = findViewById(R.id.restaurant_input);
                SeekBar mark_input = findViewById(R.id.mark_input);
                String email = email_input.getText().toString();
                String restaurant = restaurant_input.getText().toString();
                int mark = mark_input.getProgress();
                postToApi(email, restaurant, String.valueOf(mark), ticket);
            } catch (NullPointerException e) {
                toaster("An error occured, please try again", Toast.LENGTH_SHORT);
            }
        }
    }

    public void take_picture(View v) {
        if (Build.VERSION.SDK_INT >= 23) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.INTERNET) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.INTERNET}, 1);
            }
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, 1);
            }
        }

        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, 1);
        }
    }
}
