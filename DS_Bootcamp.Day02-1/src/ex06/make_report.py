import analytics
import config

def do_research(research):
    arr = research.file_reader(has_header=config.has_header)
    an = research.Analytics(arr)
    count = an.counts()

    frac = an.fractions(*count)

    r_arr = an.predict_random(config.num_of_steps)
    an = research.Analytics(r_arr)
    r_counts = an.counts()

    report = config.report_template.format(total = len(arr), n_tails = count[0], n_heads = count[1],
                                     p_heads = frac[0], p_tails = frac[1],
                                     n_r =len(r_arr) , n_r_tails = r_counts[0], n_r_heads = r_counts[1])
    an.save_data(report, config.report_name, config.report_ex)

def main():
    research = analytics.Research(config.path)
    try:
        do_research(research)
    except Exception:
         research.telegram_message(False)
    else:
        research.telegram_message(True)





if __name__ == "__main__":
        main()
