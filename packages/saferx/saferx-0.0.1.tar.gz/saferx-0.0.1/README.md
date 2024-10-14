# SAFER

This guide provides  SAFER model module

## Baseline

- Baseline
  - data_processing_m1
    - crf_data.py
    - location_data.py
    - sensor_data.py
  - data_processing_m2
    - crf_data.ppy
    - location_data.py
    - sensor_data.py
  - model1
    - dataloader.py
    - model.py
    - predictor.py
  - model2
    - dataloader.py
    - model.py
    - preictor.py
  - setup.py
  - README.md

## How To Use 

***Start pip install***

- data processing

    1. location

        You can load location data from preprocess it as follows:

    <pre><code>
    from location_processor import LocationProcessor

    file_path = ''
    processed_location_data = LocationProcessor.load_data_from_csv(file_path)

    location_dict = {
        (37.7749, -122.4194): 'ward',
        (34.0522, -118.2437): 'hallway',
        (40.7128, -74.0060): 'other',
    }

    labeled_location_data = LocationProcessor.assign_location_labels(processed_data, location_dict)


    </code></pre>

    2. sensor

        you can load sensor data from preprocess it as follows :

        <pre><code>
        from sensor_processor import SensorDataProcessor

        file_path = ''
        sensing_data = SensorDataProcessor.load_sensing_data(file_path)
        sensing_data = SensorDataProcessor.process_sensing_data(sensing_data)
        sensing_data = SensorDataProcessor.aggregate_sensing_data(sensing_data)
        sensing_data = SensorDataProcessor.reorganize_column_names(sensing_data)
        </code></pre>

    3. patient data (2 type of data)

        you can load patient data from preprocess it as follows :

        <pre><code>
        from crf_data import DataProcessor
        status_file_path = ''
        trait_fiile_path = ''
           
        processor = DataProcessor()

        processor.load_data(
            location_file=labeled_location_data,
            sensor_file=sensing_data,
            crf_file= status_file_path ,
            trait_file= trait_fiile_path
        )

        processor.merge_location_and_sensor()
        processor.process_crf_data()
        processor.merge_trait_data()



        suicide_flags = [
            ('patient_key', pd.to_datetime('2023-12-02 00:00:00')),
            .
            .
        ]



        final_data = processor.clean_and_set_suicide_flag(suicide_flags)
        final_data = filter_data_for_self_harm_and_random(final_data, suicide_flags)

        </code></pre>

- model

    you can predict m1 from preprocess it as follows :
    -  m1
    <pre><code>
        from model1.model import TemporalFusionTransformer
        from model1.predictor import PredictionHandler

        data_paths = ['']
        predictor = PredictionHandler(data_paths, batch_size=16, device='cpu')
        predictions = predictor.predict()

     </code></pre>

    - m2
    <pre><code>
        from model2.predictor import Predictor
        import torch
        from model2.model import CNNGRUClassificationModel

        data_path = ''  

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        predictor = Predictor(device=device)

        data_loader = predictor.preprocess_data(data_path)

        predictions = predictor.predict(data_loader)

        print(predictions)

    </code></pre>
        