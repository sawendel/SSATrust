import { Fragment } from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const EmailHeaderDetails = ({ config, date }) => {
  const details = [
    { label: 'From', value: `${config?.fromName} | ${config?.fromEmail}` },
    { label: 'Reply to', value: config?.replyTo },
    { label: 'To', value: config?.to },
    { label: 'Date', value: date },
    { label: 'Mailed by', value: config?.mailedBy },
    { label: <i className="et-lock" />, value: 'Standard Encryption' },
  ];

  return (
    <Container fluid className="et-email-header-details">
      <Row>
        {details.map((x) => (
          <Fragment key={x.label}>
            <Col lg={3} xs={4} className="pb-2"><small className="text-lynch">{x.label}</small></Col>
            <Col lg={9} xs={8} className="pb-2"><small>{x.value}</small></Col>
          </Fragment>
        ))}
      </Row>
    </Container>
  );
};

export default EmailHeaderDetails;
