package com.etipech.hacktonsub;

import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.NetworkOnMainThreadException;
import android.util.Log;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

/**
 * Created by Moi on 24/02/2018.
 */

public class NetworkAsyncTask extends AsyncTask<String, Void, String> {

    @Override
    protected String doInBackground(String... params) {
        String email, restaurant, mark, ticket;

        System.err.println("DO IN BACKGROUND");
        if (params.length != 4){
            System.err.println("Invalid arguments");
            return "An error has occurred";
        }
        email = params[0];
        restaurant = params[1];
        mark = params[2];
        ticket = params[3];
        try {
            URL obj = new URL("http://10.15.192.243:4242");
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("User-Agent", "Mozilla/5.0");
            con.setRequestProperty("Accept-Language", "en-US,en; q=0.5");
            Log.e("DEBUG", "email=" + email + "&restaurant= " + restaurant + "&mark=" + mark + "&ticket=" + ticket);
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
            System.out.println("\nSending 'POST' request to URL : http://10.15.192.243:4242");
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
            System.out.println("RESPONSE : " + response.toString());
        } catch (Exception e) {
            System.err.println("Error");
            e.printStackTrace();
        }
        return "toto";
    }
}
