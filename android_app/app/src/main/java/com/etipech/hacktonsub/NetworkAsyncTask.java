package com.etipech.hacktonsub;

import android.os.AsyncTask;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

/**
 * Created by Moi on 24/02/2018.
 */

public class NetworkAsyncTask extends AsyncTask<String, Void, String> {

    @Override
    protected String doInBackground(String... params) {
        String email, storeNumber, grade, ticket;
        StringBuilder response = new StringBuilder();

        if (params.length < 4){
            System.err.println("Invalid arguments");
            return "An error has occurred";
        }
        email = params[0];
        storeNumber = params[1];
        grade = params[2];
        ticket = params[3];
        try {
            URL obj = new URL("https://hacktonsub.api.thamin.ovh");
//            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("User-Agent", "Mozilla/5.0");
            con.setRequestProperty("Accept-Language", "en-US,en; q=0.5");
            String urlParameters = "email=" + email + "&grade=" + grade + "&ticket=" + ticket + "&storeNumber=" + storeNumber;
            con.setDoOutput(true);
            DataOutputStream wr = new DataOutputStream(con.getOutputStream());
            wr.writeBytes(urlParameters);
            wr.flush();
            wr.close();
            int responseCode = con.getResponseCode();
            System.out.println("Post parameters : " + urlParameters);
            System.out.println("Response Code : " + responseCode);
            BufferedReader in;
            if (responseCode != 200){
                in = new BufferedReader(
                        new InputStreamReader(con.getErrorStream()));
            }
            else {
                in = new BufferedReader(
                        new InputStreamReader(con.getInputStream()));
            }
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            System.out.println("RESPONSE : " + response.toString());
        } catch (Exception e) {
            System.err.println("Error");
            e.printStackTrace();
        }
        return response.toString();
    }
}
