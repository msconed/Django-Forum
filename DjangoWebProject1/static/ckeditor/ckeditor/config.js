/**
 * @license Copyright (c) 2003-2023, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
    config.toolbar = [
        { name: 'styles', items: ['Format', 'Bold', 'Italic', 'Underline', 'Strike', '-', 'TextColor', 'BGColor'] },
        { name: 'clipboard', items: ['Undo', 'Redo'] },
        { name: 'links', items: ['Link', 'Unlink'] },
        { name: 'insert', items: ['Image', 'Table', 'HorizontalRule', 'Smiley'] }
    ];
    config.language = 'ru';
};
