package com.etipech.hacktonsub;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

public class MainActivity extends AppCompatActivity {

    private void toaster(String message, int duration) {
        Context context = getApplicationContext();
        Toast toast = Toast.makeText(context, message, duration);
        toast.show();
    }

    private void postToApi(String email, String restaurant, String mark, Bitmap ticket) {
        String url = "www.hacktonsub.ovh";
        try {
            URL obj = new URL(url);
            HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("User-Agent", "Mozilla/5.0");
            con.setRequestProperty("Accept-Language", "en-US,en; q=0.5");
            Log.e("DEBUG", "email=" + email + "&restaurant= " + restaurant + "&mark=" + mark + "&ticket=" + ticket.toString());
            String urlParameters = "email=" + email + "&restaurant= " + restaurant + "&mark=" + mark + "&ticket=" + ticket.toString();
            con.setDoOutput(true);
            DataOutputStream wr = new DataOutputStream(con.getOutputStream());
            wr.writeBytes(urlParameters);
            wr.flush();
            wr.close();
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
            toaster("Server currently unavailable", Toast.LENGTH_SHORT);
        }
    }

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
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, 1);
        }
    }
}
