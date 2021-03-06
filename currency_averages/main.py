import config
import orchestrator

# program initialization
config = config.Config()
orchestrator = orchestrator.Orchestrator(config)

orchestrator.detect_new_currencies(['USD', 'GBP', 'NOK'])
orchestrator.extract_historical_from_new_currencies()
orchestrator.update_currencies()
orchestrator.create_inverse_matrix()
orchestrator.export_master()
orchestrator.save_backup()
orchestrator.close_program()