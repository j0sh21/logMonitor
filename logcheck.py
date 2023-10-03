#!/usr/bin/python3

import os
import smtplib
import config

def save_matching_lines(file_name, matching_lines):
    try:
        with open(file_name, "w") as cache_file:
            for line in matching_lines:
                cache_file.write(line)
    except Exception as e:
        print(f"Fehler beim Speichern der Cache-Datei {file_name}: {str(e)}")

def load_cached_lines(file_name):
    cached_lines = []
    try:
        with open(file_name, "r") as cache_file:
            cached_lines = cache_file.readlines()
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Fehler beim Laden der Cache-Datei {file_name}: {str(e)}")

    return cached_lines

def mail_if_changed(matching_lines_m, file_name, subject_m, mailfrom_m, mailto_m, smtp_m, mail_usr_m, mail_pwd_m, count_mails_n):
    cached_lines = load_cached_lines(f"{file_name}.cache")

    if matching_lines_m != cached_lines:
        save_matching_lines(f"{file_name}.cache", matching_lines_m)

        if not matching_lines_m:
            print(f"Keine Übereinstimmungen in der Datei {file_name}. Keine E-Mail wird gesendet.")
            return count_mails_n

        info_m = f"\n\nLog-Datei: {file_name}\n\nDocker Errors:\n"
        for line in matching_lines_m:
            info_m += line
        msg_m = 'From:' + mailfrom_m + '\n' + 'To:' + mailto_m + '\n' + 'Subject:' + subject_m + '\n' + info_m

        try:
            server = smtplib.SMTP(smtp_m)
            server.starttls()
            server.login(mail_usr_m, mail_pwd_m)
            server.sendmail(mailfrom_m, mailto_m, msg_m)
            server.quit()
            print(f'\nE-Mail für {file_name} versendet.\n')
            count_mails_n += 1
            return count_mails_n
        except Exception as e:
            print(f"Fehler beim Senden der E-Mail: {str(e)}")
            return count_mails_n
    else:
        print(f"Keine Veränderung in der Datei. Keine E-Mail wird gesendet.\n")
        return count_mails_n

def search_in_file(file_path, keywords):
    matching_lines = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                for keyword in keywords:
                    if keyword in line.lower():
                        matching_lines.append(line)
    except Exception as e:
        print(f"Fehler beim Lesen der Datei {file_path}: {str(e)}")

    return matching_lines

def search_logs(directory, keywords, count_hits_n, count_mails_s):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".log"):
                file_path = os.path.join(root, file_name)
                matching_lines = search_in_file(file_path, keywords)
                print(f"Treffer in Datei: {file_path}")
                count_hits_n += 1
                count_mails_s = mail_if_changed(matching_lines, file_name, config.subject, config.mailfrom, config.mail_to,
                                config.smtp, config.mail_usr, config.mail_pwd, count_mails_s)
    return count_mails_s, count_hits_n

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    search_directories = ["/home/Umbrel/logs"]
    keywords = ["error", "err", "exception", "fatal", "failed", "critical", "unhandled", "issue", "problem"]

    count_mails_total = 0  # Initialize a variable to count total emails sent
    count_hits_total = 0
    for directory in search_directories:
        count_hits = 0
        count_mails = 0
        count_mails, count_hits = search_logs(directory, keywords, count_hits, count_mails)
        if count_mails is None:
            count_mails = 0
        count_mails_total += int(count_mails)  # Accumulate the count of emails sent for all directories
        count_hits_total += int(count_hits)

    # Check if no emails were sent and display "NONE" in that case
    if count_mails_total == 0:
        count_mails_total = "NONE"

    print(f"\nAnzahl Treffer: {count_hits_total}\nAnzahl Mails versendet:  {count_mails_total}")
