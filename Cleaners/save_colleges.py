import pandas as pd


if __name__ == '__main__':

    # Load data
    data = pd.read_csv("../Data/ncaa_drafted_qbs.csv")
    clean_data = pd.read_csv("../Data/cleaned_ncaa_drafted_qbs.csv")

    colleges = {}
    conferences = {}

    # Iterate through data
    for i in range(len(data)):
        player = data["player"][i]
        conference = data["conference"][i]
        college = data["college"][i]

        # Map data to numerical encoding
        try:
            player_index = list(clean_data["player"]).index(player)
            cleaned_conference = clean_data["conference"][player_index]
            cleaned_college = clean_data["college"][player_index]

            if college not in colleges:
                colleges[college] = cleaned_college

            if conference not in conferences:
                conferences[conference] = cleaned_conference

        except Exception:
            pass

    # Save data
    file = open("../Data/colleges.py", "w")
    file.write("# Dictionary mapping colleges to numerical encodings\n")
    file.write(f"colleges = {colleges}\n")
    file.write("\n")
    file.write("# Dictionary mapping conferences to numerical encodings\n")
    file.write(f"conferences = {conferences}\n")
    file.write("\n")
    file.write("""colleges["Kansas"] = 330
colleges["Ole Miss"] = colleges["Mississippi"]
colleges["Colorado"] = 331
colleges["Ohio State"] = colleges["Ohio St."]""")
    file.close()
