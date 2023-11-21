import azure.functions as func
import logging

app = func.FunctionApp()

@app.schedule(schedule="0 */1 * * * *",
                arg_name="timer",
                run_on_startup=False)

def main(timer: func.TimerRequest) -> None:

    logging.info('FUNCTION STARTED...')

    try:
        import servicebus_test
        
        logging.info('FUNCTION EXECUTED SUCCESSFULLY')
        
    except Exception as e:
        logging.error(f'Error occurred: {str(e)}')