cube(`DimCustomer`, {
  sql: `SELECT * FROM analytics.dim_customer`,

  measures: {
    totalCustomers: {
      type: `count`
    }
  },

  dimensions: {
    customerId: {
      sql: `customer_id`,
      type: `string`,
      primaryKey: true
    },

    customerSegment: {
      sql: `customer_segment`,
      type: `string`
    },

    membershipStatus: {
      sql: `membership_status`,
      type: `string`
    },

    gender: {
      sql: `customer_gender`,
      type: `string`
    }
  }
});