from datetime import datetime, timedelta
import os

from fpdf import FPDF

import plot
import util

WIDTH = 210
HEIGHT = 297
DARK_BACKGROUND = './resources/dark_background.png'

class ReportGenerator:
    
    def __init__(
        self,
        filename='report.pdf',
        states=util.TEST_STATES,
        day=util.TEST_DATE,
        dark_mode=True
        ):
        self.pdf = FPDF()    # Size A4 (210 by 297 mm)

        text = 255 if dark_mode else 17
        self.pdf.set_text_color(text, text, text)
        self.pdf.set_text_color(text, text, text)

        os.makedirs('./plots/', exist_ok=True)

        self.createPageOne(states, day, dark_mode)
        self.createPageTwo(states, day, dark_mode)
        self.createPageThree(states, day, dark_mode)

        filename = f"./report_{day.replace('/', '-')}{'_dark' if dark_mode else ''}.pdf"
        self.pdf.output(filename, 'F')

    def createPageOne(self, states, day, dark_mode):
        self.pdf.add_page()

        self.pdf.image(f"./resources/letterhead{'_dark' if dark_mode else ''}.png",
            x=0, y=0, w=WIDTH, h=HEIGHT, type='', link='')
        
        """ Title """
        # Use windows-1252 standard font; no unicode support on the py3k version
        self.pdf.set_font('Arial', '', 24)    
        self.pdf.ln(50)
        self.pdf.write(5, f'Covid Analytics Report')
        self.pdf.ln(10)
        self.pdf.set_font('Arial', '', 16)
        self.pdf.write(4, f'{day}')
        self.pdf.ln(5)

        plot.plotCaseMap(filename='./plots/case_map-us.png', day=day,
            dark_mode=dark_mode)
        prev_days = 250
        plot.plotTimeSeries(filename='./plots/time_series-cases-250.png',
            places=states, num_days=prev_days, end_date=day,
            dark_mode=dark_mode)
        plot.plotTimeSeries(filename='./plots/time_series-deaths-250.png',
            places=states, cases=False, num_days=prev_days, end_date=day,
            dark_mode=dark_mode)

        self.pdf.image('./plots/case_map-us.png', 5, 90, WIDTH - 20)
        self.pdf.image('./plots/time_series-cases-250.png', 5, 200,
            WIDTH / 2 - 10)
        self.pdf.image('./plots/time_series-deaths-250.png', WIDTH / 2, 200,
            WIDTH / 2 - 10)

    def createPageTwo(self, states, day, dark_mode):
        self.pdf.add_page()
        
        self.pdf.image(f"./resources/page{'_dark' if dark_mode else ''}.png",
            x=0, y=0, w=WIDTH, h=HEIGHT, type='', link='')

        plot.plotDaily(filename='./plots/daily-cases.png', dark_mode=dark_mode)
        plot.plotDaily(filename='./plots/daily-deaths.png', places=states,
            cases=False, dark_mode=dark_mode)
        self.pdf.image('./plots/daily-cases.png', 5, 20, WIDTH / 2 - 10)
        self.pdf.image('./plots/daily-deaths.png', WIDTH / 2, 20,
            WIDTH / 2 - 10)

        prev_days = 7
        plot.plotTimeSeries(filename='./plots/time_series-cases-7.png',
            places=states, num_days=prev_days, end_date=day,
            dark_mode=dark_mode)
        plot.plotTimeSeries(filename='./plots/time_series-deaths-7.png',
            places=states, num_days=prev_days, end_date=day,
            dark_mode=dark_mode)
        self.pdf.image('./plots/time_series-cases-7.png', 5, 110,
            WIDTH / 2 - 10)
        self.pdf.image('./plots/time_series-deaths-7.png', WIDTH / 2, 110,
            WIDTH / 2 - 10)

        prev_days = 30
        plot.plotTimeSeries(filename='./plots/time_series-cases-30.png',
            places=states, num_days=prev_days, end_date=day,
            dark_mode=dark_mode)
        plot.plotTimeSeries(filename='./plots/time_series-deaths-30.png',
            places=states, num_days=prev_days, end_date=day,
            dark_mode=dark_mode)
        self.pdf.image('./plots/time_series-cases-30.png', 5, 200,
            WIDTH / 2 - 10)
        self.pdf.image('./plots/time_series-deaths-30.png', WIDTH / 2, 200,
            WIDTH / 2 - 10)

    def createPageThree(self, states, day, dark_mode):
        self.pdf.add_page()
        
        self.pdf.image(f"./resources/page{'_dark' if dark_mode else ''}.png",
            x=0, y=0, w=WIDTH, h=HEIGHT, type='', link='')

        plot.plotCaseMap(filename='./plots/case_map-global.png', US=False,
            day=day, dark_mode=dark_mode)

        countries = ['US', 'India', 'Brazil']
        prev_days = 7
        plot.plotTimeSeries(US=False,
            filename='./plots/time_series-cases-global.png', places=countries,
            num_days=prev_days, end_date=day, dark_mode=dark_mode)
        plot.plotTimeSeries(US=False,
            filename='./plots/time_series-deaths-global.png', places=countries,
            num_days=prev_days, end_date=day, dark_mode=dark_mode)

        self.pdf.image('./plots/case_map-global.png', 5, 20, WIDTH-20)
        self.pdf.image('./plots/time_series-cases-global.png', 5, 130,
            WIDTH / 2 - 10)
        self.pdf.image('./plots/time_series-deaths-global.png', WIDTH / 2, 130,
            WIDTH / 2 - 10)

if __name__ == '__main__':
    yesterday = ((datetime.today() - timedelta(days=1))
        .strftime('%m/%d/%y')
        .replace('/0','/')
        .lstrip('0'))

    filename = f"./report_{yesterday.replace('/', '-')}.pdf"
    
    ReportGenerator(filename=filename, day=yesterday, dark_mode=False)