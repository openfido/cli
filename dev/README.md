# OpenFIDO Development Tools

You may use the files in this folder to develop openfido products.

## Dev tools installation

The dev tools are locate in the dev folder.  To install the dev tools, do the following:

~~~
host% cd openfido
curl -sL https://raw.githubusercontent.com/openfido/cli/main/install_dev.sh | bash
~~~

## Creating a new product

To create a new product use the following command:

~~~
host% make NAME=product_name product
~~~

## Modifying an existing product

To work on an existing product use the following command:

~~~
host% git clone https://github.com/openfido/product_name
~~~

When done working on the product update the documents using the following command:

~~~
host% make docs
~~~

## Installing a new product locally

To install from a local copy of a product use the following command:

~~~
host% make install
~~~
