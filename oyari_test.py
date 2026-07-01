
            <br>
            <div style="margin: 20px 0;">
              <a href="https://enzanso-reservation.jp" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
            </div>
          </body>
        </html>
        """
        send_plain_alert_email(EMAIL_SUBJECT_DAILY, html_content)

if __name__ == "__main__":
    run_mode = "check"
    if len(sys.argv) > 1:
        if "daily" in sys.argv:
