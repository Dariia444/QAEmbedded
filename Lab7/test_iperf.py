import custom_parser


class TestSuite():
    def test_iperf_client_connection(self, client):
        output, error = client
        assert not error
        results = custom_parser.parse(output)
        print('\n')
        for line in results:
            assert float(line['Transfer']) > 100 and float(line['Bandwidth']) > 1.3
            print(line)
